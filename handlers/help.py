from aiogram import Router, types
from aiogram.filters import Command

router = Router()


@router.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "⚙ <b>Функции бота ZanAI:</b>\n\n"
        "/start — приветствие и главное меню\n"
        "/help — список команд\n\n"
        "/question &lt;ваш вопрос&gt; — задать юридический вопрос\n"
        "/document — отправить документ (PDF/фото) на демонстрационный анализ\n"
        "/template — список юридических шаблонов (договор, заявление, иск)\n"
        "/template &lt;код&gt; — получить конкретный шаблон (например, /template 1)\n"
        "/accident — пошаговый разбор ситуации по ДТП\n"
        "/client &lt;Имя Телефон Комментарий&gt; — создать карточку клиента\n\n"
        "Также можно пользоваться кнопками внизу экрана (главное меню)."
    )
