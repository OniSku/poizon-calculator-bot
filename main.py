import asyncio
import logging
from aiogram import Bot, Dispatcher
from core.config import BOT_TOKEN
from database.db import init_models
from handlers.client import client_router


async def main():
    logging.basicConfig(level=logging.INFO)

    # Инициализация таблиц в PostgreSQL
    await init_models()

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(client_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())