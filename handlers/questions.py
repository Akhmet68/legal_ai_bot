from aiogram import Router, types
from aiogram.filters import Command

from services.ai_engine import answer_question

router = Router()


@router.message(Command("question"))
async def cmd_question(message: types.Message):
    parts = message.text.split(maxsplit=1)

    if len(parts) == 1:
        await message.answer(
            "Пожалуйста, укажи вопрос в одной строке, например:\n"
            "<code>/question Как оформить расписку о займе денег?</code>"
        )
        return

    question_text = parts[1]
    await message.answer("Обрабатываю ваш вопрос...")

    answer = answer_question(question_text)
    await message.answer(answer)
