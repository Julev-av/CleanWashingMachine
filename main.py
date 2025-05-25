from flask import Flask
from threading import Thread
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from datetime import datetime
from zoneinfo import ZoneInfo
import os

# Flask-сервер для поддержки аптайм-бота
app = Flask('')

@app.route('/')
def home():
    return "Я жив!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# Клавиатура главного меню
def main_menu_keyboard():
    keyboard = [
        ["1 стиралка", "2 стиралка"],
        ["3 стиралка", "4 стиралка"],
        ["Сообщить о вонючке"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# Клавиатура меню вонючек
def smelly_menu_keyboard():
    keyboard = [
        ["Стиралка 1 воняет", "Стиралка 2 воняет"],
        ["Стиралка 3 воняет", "Стиралка 4 воняет"],
        ["⬅️ Назад"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Выберите действие:", reply_markup=main_menu_keyboard())

# Обработка сообщений-кнопок
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    berlin_tz = ZoneInfo("Europe/Berlin")
    time_now = datetime.now(berlin_tz).strftime("%H:%M")

    valid_options = [
        "1 стиралка", "2 стиралка", "3 стиралка", "4 стиралка",
        "Сообщить о вонючке",
        "Стиралка 1 воняет", "Стиралка 2 воняет",
        "Стиралка 3 воняет", "Стиралка 4 воняет",
        "⬅️ Назад"
    ]

    if text not in valid_options:
        return  # игнорируем лишние сообщения

    if text in ["1 стиралка", "2 стиралка", "3 стиралка", "4 стиралка"]:
        number = text[0]
        await update.message.reply_text(f"🕒 {time_now} — Стиралка {number} свободна", reply_markup=main_menu_keyboard())

    elif text == "Сообщить о вонючке":
        await update.message.reply_text("Какая стиралка воняет?", reply_markup=smelly_menu_keyboard())

    elif text in ["Стиралка 1 воняет", "Стиралка 2 воняет", "Стиралка 3 воняет", "Стиралка 4 воняет"]:
        number = text[9]
        await update.message.reply_text(f"⚠️ Стиралка {number} воняет! Срочно проветрить!", reply_markup=main_menu_keyboard())

    elif text == "⬅️ Назад":
        await update.message.reply_text("Возврат в главное меню:", reply_markup=main_menu_keyboard())

# Запуск бота
def main():
    keep_alive()  # запускаем веб-сервер для UptimeRobot
    TOKEN = os.environ['TOKEN']
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    print("Бот запущен...")
    app.run_polling()

if __name__ == '__main__':
    main()
