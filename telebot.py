import requests
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

load_dotenv()
# Замените на ваш токен
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')


# Получение курса доллара (здесь используется открытый API, который предоставляет курс)
def get_usd_rate():
    response = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
    data = response.json()
    usd_rate = data['Valute']['USD']['Value']
    return usd_rate


# Обработчик команды /start
async def start(update: Update, context) -> None:
    await update.message.reply_text("Добрый день. Как вас зовут?")


# Обработчик сообщений с именем пользователя
async def handle_name(update: Update, context) -> None:
    name = update.message.text
    usd_rate = get_usd_rate()
    await update.message.reply_text(f"Рад знакомству, {name}! Курс доллара сегодня {usd_rate}р.")


# Основная функция для запуска бота
def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Обработчик команды /start
    application.add_handler(CommandHandler("start", start))

    # Обработчик текстовых сообщений (имя пользователя)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_name))

    # Запуск бота
    application.run_polling()


if __name__ == '__main__':
    main()
