"""Phase 4: собираем HTML send-page (один файл, открывается в браузере)."""
from __future__ import annotations

import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import typer

from src.config import DATA_DIR, load_settings, setup_logging
from src.db import fetch_leads_by_status, get_client
from src.ui.send_page import row_html

log = logging.getLogger(__name__)
app = typer.Typer(add_completion=False)


HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<title>LeadHunter — Send Queue</title>
<style>
* { box-sizing: border-box; }
body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
       margin: 0; padding: 24px; background: #0e1116; color: #e6e8eb; }
h1 { font-size: 22px; margin: 0 0 16px; }
.stats { display: flex; gap: 12px; margin-bottom: 20px; flex-wrap: wrap; }
.stat { background: #1a1f29; padding: 10px 14px; border-radius: 8px; font-size: 13px; }
.stat strong { color: #4ade80; font-size: 18px; display: block; }
table { width: 100%; border-collapse: collapse; background: #1a1f29; border-radius: 8px; overflow: hidden; }
th, td { padding: 10px 12px; text-align: left; border-bottom: 1px solid #2a313b; vertical-align: top; }
th { background: #232a36; font-size: 12px; text-transform: uppercase; color: #94a3b8; }
tr:last-child td { border-bottom: none; }
.template-A { background: rgba(74,222,128,0.1); }
.template-B { background: rgba(96,165,250,0.1); }
.template-C { background: rgba(251,191,36,0.1); }
.send-btn {
  display: inline-block; padding: 8px 14px; background: #25D366; color: #0e1116;
  text-decoration: none; border-radius: 6px; font-weight: 600; font-size: 13px;
  white-space: nowrap;
}
.send-btn:hover { background: #1ebe5b; }
.mark-btn {
  margin-left: 6px; padding: 6px 10px; background: #2a313b; color: #94a3b8;
  border: none; border-radius: 6px; font-size: 12px; cursor: pointer;
}
.mark-btn:hover { background: #3a414b; color: #e6e8eb; }
.offer-text { font-size: 13px; color: #cbd5e1; max-width: 480px; white-space: pre-wrap;
              max-height: 80px; overflow-y: auto; padding: 6px; background: rgba(0,0,0,0.2); border-radius: 4px; }
.tag { padding: 2px 6px; background: #2a313b; border-radius: 4px; font-size: 11px; color: #94a3b8; }
.row-sent { opacity: 0.4; }
input[type="text"], input[type="search"] {
  padding: 8px 12px; background: #1a1f29; border: 1px solid #2a313b; color: #e6e8eb;
  border-radius: 6px; width: 300px;
}
:focus-visible { outline: 2px solid #4ade80; outline-offset: 2px; }
.filter-row { margin-bottom: 16px; display: flex; gap: 8px; align-items: center; }
</style>
</head>
<body>
<h1>LeadHunter — Send Queue ({count} лидов)</h1>

<div class="stats">
  <div class="stat"><strong id="stat-total">{count}</strong>всего</div>
  <div class="stat"><strong id="stat-A">0</strong>Template A</div>
  <div class="stat"><strong id="stat-B">0</strong>Template B</div>
  <div class="stat"><strong id="stat-C">0</strong>Template C</div>
  <div class="stat"><strong id="stat-sent">0</strong>отправлено в этой сессии</div>
</div>

<div class="filter-row">
  <input type="search" id="search" aria-label="Поиск лидов" placeholder="Поиск по имени / категории..." oninput="applyFilter()">
  <label><input type="checkbox" id="filter-hide-sent" onchange="applyFilter()"> скрыть отправленные</label>
</div>

<table id="leads-table">
<thead>
<tr>
  <th>#</th>
  <th>Бизнес</th>
  <th>Категория</th>
  <th>Город</th>
  <th>Шаблон</th>
  <th>Сообщение (preview)</th>
  <th>Действие</th>
</tr>
</thead>
<tbody>
{rows}
</tbody>
</table>

<script>
const SUPABASE_URL = "{supabase_url}";
const SUPABASE_ANON_KEY = "{supabase_anon_key}";

function updateStats() {{
  const rows = document.querySelectorAll("tbody tr");
  let A=0, B=0, C=0;
  rows.forEach(r => {{
    if (r.classList.contains("template-A")) A++;
    else if (r.classList.contains("template-B")) B++;
    else if (r.classList.contains("template-C")) C++;
  }});
  document.getElementById("stat-A").textContent = A;
  document.getElementById("stat-B").textContent = B;
  document.getElementById("stat-C").textContent = C;
}}
updateStats();

function applyFilter() {{
  const q = (document.getElementById("search").value || "").toLowerCase();
  const hideSent = document.getElementById("filter-hide-sent").checked;
  const rows = document.querySelectorAll("tbody tr");
  rows.forEach(r => {{
    const txt = r.textContent.toLowerCase();
    const isSent = r.classList.contains("row-sent");
    let visible = txt.includes(q);
    if (hideSent && isSent) visible = false;
    r.style.display = visible ? "" : "none";
  }});
}}

async function markSent(leadId, btn) {{
  const row = btn.closest("tr");
  row.classList.add("row-sent");
  const sentCounter = document.getElementById("stat-sent");
  sentCounter.textContent = parseInt(sentCounter.textContent || 0) + 1;
  // PATCH в Supabase через REST API (anon key + RLS policy должна разрешать)
  try {{
    const resp = await fetch(`${{SUPABASE_URL}}/rest/v1/leads?id=eq.${{encodeURIComponent(leadId)}}`, {{
      method: "PATCH",
      headers: {{
        "apikey": SUPABASE_ANON_KEY,
        "Authorization": `Bearer ${{SUPABASE_ANON_KEY}}`,
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
      }},
      body: JSON.stringify({{ status: "sent", sent_at: new Date().toISOString() }})
    }});
    if (!resp.ok) {{
      console.error("Failed to mark sent:", await resp.text());
      btn.textContent = "⚠ Re-mark";
    }} else {{
      btn.textContent = "✓ sent";
      btn.disabled = true;
    }}
  }} catch (e) {{
    console.error(e);
  }}
}}

document.addEventListener("click", (event) => {{
  const sendBtn = event.target.closest(".js-send-btn");
  if (sendBtn) {{
    const leadId = sendBtn.dataset.leadId || "";
    setTimeout(() => markSent(leadId, sendBtn), 200);
    return;
  }}

  const markBtn = event.target.closest(".js-mark-btn");
  if (markBtn) {{
    const leadId = markBtn.dataset.leadId || "";
    markSent(leadId, markBtn);
  }}
}});
</script>
</body>
</html>
"""


@app.command()
def main(
    output: Path = typer.Option(
        DATA_DIR / "send_page.html", help="Куда писать HTML"
    ),
    limit: int = typer.Option(500, help="Лимит лидов в странице"),
) -> None:
    settings = load_settings()
    setup_logging(settings.log_level)
    client = get_client(settings)

    leads = fetch_leads_by_status(client, status="generated", limit=limit)
    log.info("Найдено %d лидов в статусе 'generated'", len(leads))

    if not leads:
        log.warning("Нет лидов для отправки. Запусти сначала 3_generate_offers.py")
        raise typer.Exit(code=1)

    rows_html = "\n".join(row_html(i, lead) for i, lead in enumerate(leads, 1))

    html = (
        HTML_TEMPLATE
        .replace("{count}", str(len(leads)))
        .replace("{rows}", rows_html)
        .replace("{supabase_url}", settings.supabase_url)
        .replace("{supabase_anon_key}", settings.supabase_anon_key)
    )

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(html, encoding="utf-8")
    log.info("HTML страница: %s", output.resolve())
    log.info("Открой в браузере: file://%s", output.resolve())


if __name__ == "__main__":
    app()
