import os
import gspread
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def write_to_sheet(items):
    print("🧾 Подключение к Google Sheets...")
    print(f"📊 Загружаю {len(items)} строк")

    try:
        creds = Credentials.from_service_account_file(os.getenv("GOOGLE_CREDENTIALS_JSON_PATH"), scopes=SCOPES)
        client = gspread.authorize(creds)

        spreadsheet = client.open_by_key(os.getenv("GOOGLE_SHEET_ID"))
        sheet = spreadsheet.sheet1

        sheet.clear()
        headers = ["id", "title", "description", "price", "sale_price", "availability", "brand", "image_link", "link", "facebook_product_category"]

        # Собираем данные
        values = [headers]
        for item in items:
            row = [item.get(h, "") for h in headers]
            values.append(row)

        # Обновляем всю таблицу сразу
        print("📤 Отправка данных через update()...")
        

        sheet.update("A1", values)
        print("✅ Таблица успешно обновлена!")

    except Exception as e:
        print("❌ Полная ошибка:", repr(e))
        raise
