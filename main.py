import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from src.browser.service import BrowserService
from db.orm import create_user, create_order, get_latest_fee
from db.database import db
from config import bot_token

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Запуск админ панели"""
    user_id = update.effective_user.id
    # Здесь можно добавить проверку на админа
    await update.message.reply_text("Админ панель")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Старт бота"""
    user_id = update.effective_user.id
    username = update.effective_user.username
    
    await create_user(user_id, username if username else "-")
    await update.message.reply_text(
        "Привет! Отправь мне ссылку на товар, и я покажу его цену и возможность заказа."
    )

async def item_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка сообщений с ссылками"""
    user_id = update.effective_user.id
    message_text = update.message.text
    
    try:
        # Проверяем, что сообщение содержит ссылку
        if not message_text.startswith(('http://', 'https://')):
            await update.message.reply_text("Пожалуйста, отправьте корректную ссылку на товар.")
            return

        # Получаем цену через BrowserService
        async with BrowserService() as browser:
            price = await browser.find_price(message_text)
        
        if price:
            # Получаем текущую комиссию
            fee = await get_latest_fee()
            fee_amount = fee['fee'] if fee else 0
            
            # Создаем заказ
            await create_order(message_text, float(price), fee_amount)
            
            # Отправляем ответ пользователю
            await update.message.reply_text(
                f"Цена товара: {price}\n"
                f"Комиссия: {fee_amount}%\n"
                f"Итоговая цена: {float(price) * (1 + fee_amount/100)}",
            )
        else:
            await update.message.reply_text("Не удалось получить цену товара. Проверьте ссылку и попробуйте снова.")
            
    except Exception as e:
        logging.error(f"Ошибка при обработке ссылки: {e}")
        await update.message.reply_text("Произошла ошибка при обработке ссылки. Попробуйте позже.")


if __name__ == '__main__':
    application = Application.builder().token(token="7464611060:AAE8zcGY-h9vv6AoJeVprVth1wbmGwDs0O8").build()
    
    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("admin", admin))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, item_message))
    
    # Запускаем бота
    application.run_polling(allowed_updates=Update.ALL_TYPES)