import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import TOKEN
from database.db import init_db

from handlers import start, help, questions, documents, templates, accident, client_card


async def main():
    # Инициализация БД
    init_db()

    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    dp = Dispatcher()

    # Подключение роутеров
    dp.include_router(start.router)
    dp.include_router(help.router)
    dp.include_router(questions.router)
    dp.include_router(documents.router)
    dp.include_router(templates.router)
    dp.include_router(accident.router)
    dp.include_router(client_card.router)

    print("Бот запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
