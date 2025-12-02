from aiogram import Router, types
from aiogram.filters import Command

from database.db import get_connection

router = Router()


@router.message(Command("client"))
async def cmd_client(message: types.Message):
    parts = message.text.split(maxsplit=1)

    if len(parts) == 1:
        await message.answer(
            "Создание карточки клиента.\n\n"
            "Формат команды:\n"
            "<code>/client Имя Телефон Комментарий</code>\n\n"
            "Пример:\n"
            "<code>/client Иван 87771234567 ДТП на перекрёстке, нужен разбор</code>"
        )
        return

    data = parts[1]
    pieces = data.split(maxsplit=2)

    name = pieces[0]
    phone = pieces[1] if len(pieces) > 1 else ""
    notes = pieces[2] if len(pieces) > 2 else ""

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO clients (tg_id, name, phone, notes) VALUES (?,?,?,?)",
        (message.from_user.id, name, phone, notes),
    )
    conn.commit()
    conn.close()

    await message.answer(
        "✅ Карточка клиента создана:\n\n"
        f"Имя: <b>{name}</b>\n"
        f"Телефон: <b>{phone or 'не указан'}</b>\n"
        f"Комментарий: {notes or '—'}"
    )
