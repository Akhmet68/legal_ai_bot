from aiogram import Router, types
from aiogram.filters import Command

from services.templates_service import get_template_list, get_template_by_code

router = Router()


@router.message(Command("template"))
async def cmd_template(message: types.Message):
    parts = message.text.split(maxsplit=1)

    # Если только /template — показываем список
    if len(parts) == 1:
        templates_text = get_template_list()
        await message.answer(
            "📑 Доступные шаблоны:\n\n"
            f"{templates_text}\n\n"
            "Чтобы получить шаблон, отправьте команду, например:\n"
            "<code>/template 1</code>"
        )
        return

    code = parts[1].strip()
    template_text = get_template_by_code(code)

    if not template_text:
        await message.answer("Неизвестный код шаблона. Отправьте просто /template, чтобы увидеть список.")
        return

    await message.answer(
        f"📄 Шаблон №{code}:\n\n"
        f"{template_text}"
    )
