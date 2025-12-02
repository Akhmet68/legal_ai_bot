from aiogram import Router, types
from aiogram.filters import Command

router = Router()


@router.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "⚙ <b>Функции бота:</b>\n\n"
        "/start — приветствие\n"
        "/help — список команд\n"
        "/question &lt;ваш вопрос&gt; — задать юридический вопрос\n"
        "/document — отправить документ (PDF/фото) для анализа\n"
        "/template — получить юридический шаблон\n"
        "/accident &lt;описание ДТП&gt; — помощь по ДТП\n"
        "/client &lt;Имя Телефон Комментарий&gt; — создать карточку клиента\n\n"
        "Примеры:\n"
        "• /question Как разделить имущество после развода?\n"
        "• /accident Я ехал прямо, а с второстепенной выехал автомобиль и врезался\n"
        "• /client Иван 87771234567 ДТП на перекрёстке"
    )
