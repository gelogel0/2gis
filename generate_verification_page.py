import sys
from pathlib import Path
from unittest.mock import MagicMock, patch
import importlib

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

build_module = importlib.import_module("scripts.4_build_send_page")

def generate_page():
    mock_settings = MagicMock()
    mock_settings.supabase_url = "https://example.supabase.co"
    mock_settings.supabase_anon_key = "dummy-key"
    mock_settings.log_level = "INFO"

    mock_leads = [
        {
            "id": "lead-1",
            "name": "Beauty Salon Deluxe",
            "category": "Салон красоты",
            "city": "Алматы",
            "template_id": "A",
            "generated_offer": "Привет! Хотим предложить уникальные услуги.",
            "wa_link": "https://wa.me/77011112233?text=Привет",
            "main_phone": "+77011112233"
        },
        {
            "id": "lead-2",
            "name": "Fitness Club Almaty",
            "category": "Фитнес",
            "city": "Алматы",
            "template_id": "B",
            "generated_offer": "Здравствуйте! Специальное предложение на абонементы.",
            "wa_link": "https://wa.me/77022223344",
            "main_phone": "+77022223344"
        }
    ]

    with patch.object(build_module, "load_settings", return_value=mock_settings), \
         patch.object(build_module, "get_client", return_value=MagicMock()), \
         patch.object(build_module, "fetch_leads_by_status", return_value=mock_leads):
        build_module.main(output=Path("data/send_page.html"), limit=100)

if __name__ == "__main__":
    generate_page()
