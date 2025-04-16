# Telegram YML to Meta Feed Bot

📦 Telegram-бот для загрузки YML-файлов из SalesDrive и конвертации их в формат для Meta Commerce Manager с выгрузкой в Google Sheets.

---

## 🚀 Возможности

- Загрузка YML через Telegram
- Парсинг и фильтрация товаров
- Автоматическая категория Facebook:
  - `204` — если в описании встречается "колонка"
  - `207` — все остальные
- Исключение товаров без картинки и ссылки
- Интеграция с Google Sheets

---

## 📁 Структура проекта

telegram_yml_to_meta/ ├── bot/ # Telegram-бот (main.py) ├── parser/ # Парсинг YML → Meta формат ├── sheets/ # Интеграция с Google Sheets ├── utils/ # Логгер и вспомогательные ├── data/ # Сюда сохраняются загруженные XML-файлы ├── logs/ # Лог-файлы (опционально) ├── credentials.json # Google API ключ (локально) ├── .env # Переменные окружения (локально) ├── Procfile # Render worker setup ├── requirements.txt # Python зависимости └── README.md

---

## 🛠️ Запуск локально

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m bot.main


.env
TELEGRAM_BOT_TOKEN=your_token
GOOGLE_SHEET_ID=sheet_id
GOOGLE_CREDENTIALS_JSON_PATH=credentials.json
