from aiogram import Router, types
from aiogram.filters import CommandStart

router = Router()


@router.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        "👋 Привет! Я юридический AI-помощник.\n\n"
        "Я могу:\n"
        "• Ответить на юридический вопрос (/question)\n"
        "• Принять документ на анализ (/document)\n"
        "• Выдать шаблон договора/заявления (/template)\n"
        "• Помочь с разбором ДТП (/accident)\n"
        "• Создать карточку клиента (/client)\n\n"
        "Полный список команд — /help"
    )
