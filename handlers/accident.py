import os
import sys

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from services.accident_assistant import analyse_accident_extended
from services.pdf_generator import create_accident_pdf
from database.db import get_connection

router = Router()


class AccidentForm(StatesGroup):
    place = State()
    movement = State()
    signs = State()
    damage = State()


@router.message(Command("accident"))
async def accident_start(message: types.Message, state: FSMContext):
    await state.clear()
    await state.set_state(AccidentForm.place)
    await message.answer(
        "🚗 Разбор ДТП.\n\n"
        "1/4. Укажите, где произошло ДТП (город, улица, перекрёсток, парковка и т.п.):"
    )


@router.message(AccidentForm.place)
async def accident_place(message: types.Message, state: FSMContext):
    await state.update_data(place=message.text)
    await state.set_state(AccidentForm.movement)
    await message.answer(
        "2/4. Опишите, кто как двигался перед столкновением.\n"
        "Например: «Я ехал прямо, другой автомобиль выезжал со второстепенной», "
        "или «я стоял на светофоре, в меня въехали сзади»."
    )


@router.message(AccidentForm.movement)
async def accident_movement(message: types.Message, state: FSMContext):
    await state.update_data(movement=message.text)
    await state.set_state(AccidentForm.signs)
    await message.answer(
        "3/4. Какие были знаки/светофор и кто им следовал?\n"
        "Например: «Я был на главной», «был знак уступи дорогу», "
        "«перекрёсток со светофором, я ехал на зелёный»."
    )


@router.message(AccidentForm.signs)
async def accident_signs(message: types.Message, state: FSMContext):
    await state.update_data(signs=message.text)
    await state.set_state(AccidentForm.damage)
    await message.answer(
        "4/4. Опишите повреждения и есть ли пострадавшие.\n"
        "Например: «повреждены бампер и крыло, пострадавших нет»."
    )


@router.message(AccidentForm.damage)
async def accident_finish(message: types.Message, state: FSMContext):
    await state.update_data(damage=message.text)
    data = await state.get_data()
    await state.clear()

    full_description = (
        f"Место: {data.get('place')}\n"
        f"Движение: {data.get('movement')}\n"
        f"Знаки/светофор: {data.get('signs')}\n"
        f"Повреждения/пострадавшие: {data.get('damage')}\n"
    )

    analysis_data = analyse_accident_extended(full_description)
    analysis = analysis_data["legal_analysis"]
    scheme = analysis_data["scheme"]
    actions = analysis_data["actions"]

    await message.answer(
        "✅ Спасибо, информация по ДТП собрана.\n\n"
        "📋 <b>Сводка по описанию:</b>\n"
        f"{full_description}\n"
        "🧩 <b>Схема ДТП (описательная):</b>\n"
        f"{scheme}\n\n"
        "⚖️ <b>Предварительный разбор:</b>\n"
        f"{analysis}\n\n"
        "📝 <b>Рекомендации по дальнейшим действиям:</b>\n"
        f"{actions}"
    )

    # PDF
    pdf_path = create_accident_pdf(full_description, analysis, scheme, actions)
    pdf_file = FSInputFile(pdf_path)

    await message.answer_document(
        pdf_file,
        caption="📎 PDF-отчёт по ДТП (сводка + схема + анализ + рекомендации)."
    )

    # Сохраняем кейс в БД
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO cases (tg_id, type, summary, pdf_path)
        VALUES (%s, %s, %s, %s)
        """,
        (message.from_user.id, "dtp", full_description, pdf_path),
    )
    conn.commit()
    conn.close()
