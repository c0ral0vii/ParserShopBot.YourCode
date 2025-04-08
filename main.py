import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Запуск админ панели"""
    ...

def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Старт бота"""
    ...
    

def item_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка сообщений от пользователей"""
    ...


if __name__ == '__main__':
    application = ApplicationBuilder().token('TOKEN').build()
    
    start_handler = CommandHandler('start', start)
    admin_handler = CommandHandler('admin', admin)
    item_message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, item_message)
    
    application.add_handlers(start_handler,
                             admin_handler,
                             item_message_handler
                             )
    
    application.run_polling()