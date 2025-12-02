from aiogram import Router, types
from aiogram.filters import Command

from database.db import get_connection

router = Router()


@router.message(Command("cases"))
async def list_cases(message: types.Message):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT id, type, status, created_at
        FROM cases
        WHERE tg_id = %s
        ORDER BY created_at DESC
        LIMIT 5
        """,
        (message.from_user.id,),
    )
    rows = cur.fetchall()
    conn.close()

    if not rows:
        await message.answer("📂 У вас пока нет сохранённых дел.")
        return

    lines = ["📂 <b>Последние дела:</b>"]
    for row in rows:
        case_id, ctype, status, created_at = row
        lines.append(
            f"• ID: <b>{case_id}</b>, тип: {ctype}, статус: {status}, "
            f"дата: {created_at.strftime('%d.%m.%Y %H:%M')}"
        )

    lines.append("\nПодробнее по делу: <code>/case &lt;ID&gt;</code>\nНапример: <code>/case 1</code>")
    await message.answer("\n".join(lines))


@router.message(Command("case"))
async def case_detail(message: types.Message):
    parts = message.text.split(maxsplit=1)
    if len(parts) == 1:
        await message.answer("Укажите ID дела, например:\n<code>/case 1</code>")
        return

    try:
        case_id = int(parts[1])
    except ValueError:
        await message.answer("ID дела должен быть числом, например: <code>/case 1</code>")
        return

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT id, type, status, created_at, summary, pdf_path
        FROM cases
        WHERE id = %s AND tg_id = %s
        """,
        (case_id, message.from_user.id),
    )
    row = cur.fetchone()
    conn.close()

    if not row:
        await message.answer("Дело с таким ID не найдено.")
        return

    _id, ctype, status, created_at, summary, pdf_path = row

    text = (
        f"📁 <b>Дело ID: {_id}</b>\n"
        f"Тип: {ctype}\n"
        f"Статус: {status}\n"
        f"Дата: {created_at.strftime('%d.%m.%Y %H:%M')}\n\n"
        f"<b>Сводка:</b>\n{summary}\n"
    )
    await message.answer(text)

    if pdf_path:
        try:
            pdf_file = types.FSInputFile(pdf_path)
            await message.answer_document(pdf_file, caption="📎 Отчёт по делу")
        except Exception:
            await message.answer("⚠ Не удалось прикрепить PDF-файл. Возможно, он был удалён.")


@router.message(Command("case_status"))
async def case_status(message: types.Message):
    parts = message.text.split(maxsplit=2)
    if len(parts) < 3:
        await message.answer(
            "Формат: <code>/case_status &lt;ID&gt; &lt;статус&gt;</code>\n"
            "Например: <code>/case_status 1 в_работе</code>"
        )
        return

    try:
        case_id = int(parts[1])
    except ValueError:
        await message.answer("ID дела должен быть числом.")
        return

    new_status = parts[2]

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE cases SET status = %s
        WHERE id = %s AND tg_id = %s
        """,
        (new_status, case_id, message.from_user.id),
    )
    updated = cur.rowcount
    conn.commit()
    conn.close()

    if updated:
        await message.answer(f"✅ Статус дела {case_id} изменён на: <b>{new_status}</b>")
    else:
        await message.answer("Не удалось обновить статус: дело не найдено или нет прав.")
