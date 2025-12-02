from aiogram import Router, types
from aiogram.filters import Command

router = Router()


@router.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "⚙ <b>Функции бота ZanAI:</b>\n\n"
        "/start — приветствие и главное меню\n"
        "/help — список команд\n"
        "/about — информация о боте и дисклеймер\n\n"
        "/question &lt;ваш вопрос&gt; — задать юридический вопрос (демо)\n"
        "/document — отправить документ (PDF/фото) на предварительный анализ (демо)\n"
        "/template — список юридических шаблонов (договор, заявление, иск)\n"
        "/templates_menu — меню документов с кнопками\n"
        "/template &lt;код&gt; — получить конкретный шаблон (например, /template 1)\n\n"
        "/accident — пошаговый разбор ситуации по ДТП с формированием отчёта PDF\n"
        "/client &lt;Имя Телефон Комментарий&gt; — создать карточку клиента\n\n"
        "/cases — последние дела пользователя\n"
        "/case &lt;ID&gt; — подробности по делу\n"
        "/case_status &lt;ID&gt; &lt;статус&gt; — изменить статус дела (например: в_работе, закрыто)."
    )
