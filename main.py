import logging
import asyncio
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command, CommandStart
from src.browser.service import BrowserService
from db.orm import create_user, create_order, get_latest_fee
from db.database import db
from config import bot_token
from src.converter.service import Converter

bot = Bot(token=bot_token)
dp = Dispatcher()


@dp.message(Command("/admin"))
async def admin(message: types.Message,):
    """Запуск админ панели"""
    
    user_id = message.from_user.id
    # Здесь можно добавить проверку на админа
    await message.answer("Админ панель")

@dp.message(CommandStart())
async def start(message: types.Message,):
    """Старт бота"""
    user_id = message.from_user.id

    username = message.from_user.username
    
    await create_user(user_id, username if username else "-")
    await message.answer(
        "Привет! Отправь мне ссылку на товар, и я покажу его цену и возможность заказа."
    )

@dp.message(F.text)
async def item_message(message: types.Message,):
    """Обработка сообщений с ссылками"""
    user_id = message.from_user.id
    message_text = message.text
    
    try:
        # Проверяем, что сообщение содержит ссылку
        if not message_text.startswith(('http://', 'https://')):
            await message.answer("Пожалуйста, отправьте корректную ссылку на товар.")
            return
        
        answer_message = await message.answer("Обрабатываю ссылку...")
        
        browser = BrowserService()
        data = await browser.find_item(message_text)
        
        if data:
            model = Converter()
            
            standart_price_rub = await model.convert_sum(sum=int(data["standart_price"]), currency=data["currency"])

        
            # Формируем текст с размерами и ценами
            # sizes_text = "\n".join(
            #     f"{item['size']}: {item['price']} ({await model.convert_sum(item['price'], data['currency'])})"
            #     for item in data.get("sizes", [])
            # )
            
            caption = (
                f"🏷 <b>{data['title']}</b>\n\n"
                f"💰 Цена: {data['standart_price']}{data["currency"]} ({standart_price_rub})\n\n"
                "🛒 Для заказа нажмите кнопку ниже"
            )
            print(data)
            
            kb = types.InlineKeyboardMarkup(inline_keyboard=[
                [types.InlineKeyboardButton(text="Заказать", callback_data=f"order_{data.get('product_id', '')}")]
            ])
            
            if data.get("title_img"):
                await bot.send_photo(
                    chat_id=user_id,
                    photo=data["title_img"],
                    caption=caption,
                    reply_markup=kb,
                    parse_mode="HTML"
                )
            else:
                await message.answer(
                    text=caption,
                    reply_markup=kb,
                    parse_mode="HTML"
                )
            
            await answer_message.delete()
        else:
            await message.answer("Не удалось получить цену товара. Проверьте ссылку и попробуйте снова.")
            
    except Exception as e:
        logging.error(f"Ошибка при обработке ссылки: {e}")
        await message.answer("Произошла ошибка при обработке ссылки. Попробуйте еще раз.")

async def on_startup():

    commands = [
        types.BotCommand(command="/start", description="Перезапуск бота (Restart bot)"),
    ]

    await bot.set_my_commands(commands)


async def run():
    await bot.delete_webhook(drop_pending_updates=True)
    await on_startup()

    await dp.start_polling(bot)
    
if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    asyncio.run(run())
    # Добавляем обработчики
    