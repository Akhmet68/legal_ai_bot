from aiogram import Router, types
from aiogram.filters import Command

from services.accident_assistant import analyse_accident

router = Router()


@router.message(Command("accident"))
async def cmd_accident(message: types.Message):
    parts = message.text.split(maxsplit=1)

    if len(parts) == 1:
        await message.answer(
            "Опишите ситуацию по ДТП в одной строке, например:\n"
            "<code>/accident Я стоял на светофоре, в меня сзади въехал другой автомобиль</code>"
        )
        return

    description = parts[1]
    await message.answer("Анализирую ситуацию ДТП...")

    result = analyse_accident(description)
    await message.answer(result)
