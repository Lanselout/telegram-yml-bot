from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime

from parser.yml_to_meta import parse_yml_to_meta
from sheets.google_sheets import write_to_sheet
from utils.logger import logger

# === Загрузка .env ===
env_path = Path(__file__).resolve().parent.parent / ".env"
print(f"🔍 Загрузка .env из: {env_path}")
print(f"📦 Файл существует? {env_path.exists()}")

load_dotenv(dotenv_path=env_path)

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
print(f"🔑 TOKEN загружен? {'Да' if BOT_TOKEN else 'НЕТ'}")

if not BOT_TOKEN:
    raise RuntimeError("❌ Переменная TELEGRAM_BOT_TOKEN не найдена. Проверь файл .env")

# === Telegram логика ===
UPLOAD = range(1)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["Загрузить файл"]]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Привет! Я помогу тебе загрузить YML и сформировать Meta-таблицу.", reply_markup=markup)

async def prompt_upload(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ожидаю файл XML...")
    return UPLOAD

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("📥 handle_file запущен")
    await update.message.reply_text("Начинаю обработку...")

    try:
        document = update.message.document
        file = await document.get_file()
        filename = os.path.join("data", document.file_name)
        print(f"📄 Сохраняю файл как: {filename}")
        await file.download_to_drive(custom_path=filename)

        items = parse_yml_to_meta(filename)
        print(f"📦 Найдено товаров: {len(items)}")

        write_to_sheet(items)

        in_stock = sum(1 for item in items if item["availability"] == "in stock")
        out_stock = sum(1 for item in items if item["availability"] == "out of stock")
        now = datetime.now().strftime("%d.%m.%Y %H:%M")

        await update.message.reply_text(
            f"✅ Фид сформирован, выгрузка завершена: {now}\n"
            f"📦 Всего товаров: {len(items)}\n"
            f"✅ В наличии: {in_stock}  ❌ Нет в наличии: {out_stock}"
        )

    except Exception as e:
        print("❌ Ошибка при обработке файла:", e)
        await update.message.reply_text("❌ Произошла ошибка при обработке файла.")

    return ConversationHandler.END




def main():
    app = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("Загрузить файл"), prompt_upload)],
        states={UPLOAD: [MessageHandler(filters.Document.ALL, handle_file)
]},
        fallbacks=[],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv_handler)

    print("🚀 Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
