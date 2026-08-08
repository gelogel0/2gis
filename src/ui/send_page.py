from __future__ import annotations

from html import escape
from urllib.parse import urlparse


def safe_template_id(template_id: object) -> str:
    value = str(template_id or "?")
    return value if value in {"A", "B", "C"} else "?"


def safe_wa_link(link: object) -> str:
    """Allow only canonical wa.me links used by click-to-send.

    Accepted format: https://wa.me/<digits>[?text=...]
    """
    raw = str(link or "").strip()
    if not raw:
        return ""
    parsed = urlparse(raw)
    if parsed.scheme != "https" or parsed.netloc != "wa.me":
        return ""
    if parsed.params or parsed.fragment:
        return ""
    if parsed.username or parsed.password:
        return ""
    if parsed.port not in (None, 443):
        return ""
    if not parsed.path or parsed.path == "/":
        return ""
    phone_path = parsed.path.lstrip("/")
    if not phone_path.isdigit():
        return ""
    return escape(raw, quote=True)


def row_html(idx: int, lead: dict) -> str:
    template = safe_template_id(lead.get("template_id"))
    offer = escape(lead.get("generated_offer") or "")
    wa_link = safe_wa_link(lead.get("wa_link"))
    name = escape(lead.get("name") or "")
    category = escape(lead.get("category") or "")
    city = escape(lead.get("city") or "")
    lead_id = str(lead.get("id") or "")
    lead_id_attr = escape(lead_id, quote=True)
    phone = escape(lead.get("main_phone", "-") or "-")

    send_btn = (
        f'<a class="send-btn js-send-btn" href="{wa_link}" target="_blank" '
        f'data-lead-id="{lead_id_attr}">📨 Send WA</a>'
        if wa_link
        else '<span class="tag">no phone</span>'
    )

    return f"""
<tr class="template-{template}" data-id="{lead_id_attr}">
  <td>{idx}</td>
  <td><strong>{name}</strong><br><span class="tag">{phone}</span></td>
  <td>{category}</td>
  <td>{city}</td>
  <td><span class="tag">{template}</span></td>
  <td>
    <div class="offer-wrapper">
      <div class="offer-text">{offer}</div>
      <button class="copy-btn js-copy-btn" aria-label="Copy offer">📋</button>
    </div>
  </td>
  <td>{send_btn}<button class="mark-btn js-mark-btn" data-lead-id="{lead_id_attr}">mark sent</button></td>
</tr>
""".strip()
