#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="${1:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
SERVICE_NAME="${2:-lead-hunter}"
RUN_USER="${3:-$USER}"
CITY="${CITY:-Алматы}"
CATEGORY="${CATEGORY:-салон красоты}"

PYTHON_BIN="${PROJECT_DIR}/.venv/bin/python"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"
TIMER_FILE="/etc/systemd/system/${SERVICE_NAME}.timer"

if [[ ! -x "${PYTHON_BIN}" ]]; then
  echo "Python binary not found or not executable: ${PYTHON_BIN}" >&2
  exit 1
fi

sudo tee "${SERVICE_FILE}" >/dev/null <<EOF
[Unit]
Description=LeadHunter pipeline runner
After=network.target

[Service]
Type=oneshot
User=${RUN_USER}
WorkingDirectory=${PROJECT_DIR}
EnvironmentFile=${PROJECT_DIR}/.env
ExecStart=${PYTHON_BIN} scripts/0_run_pipeline.py --city "${CITY}" --category "${CATEGORY}" --timeout-sec 3600
StandardOutput=append:${PROJECT_DIR}/data/pipeline.log
StandardError=append:${PROJECT_DIR}/data/pipeline.log

[Install]
WantedBy=multi-user.target
EOF

sudo tee "${TIMER_FILE}" >/dev/null <<EOF
[Unit]
Description=Run LeadHunter pipeline every day

[Timer]
OnCalendar=*-*-* 09:00:00
Persistent=true
Unit=${SERVICE_NAME}.service

[Install]
WantedBy=timers.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable --now "${SERVICE_NAME}.timer"
sudo systemctl status "${SERVICE_NAME}.timer" --no-pager

