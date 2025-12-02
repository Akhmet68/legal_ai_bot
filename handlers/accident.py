from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

from services.accident_assistant import analyse_accident
from services.pdf_generator import create_accident_pdf

router = Router()


class AccidentForm(StatesGroup):
    place = State()       # где произошло
    movement = State()    # кто как ехал
    signs = State()       # знаки / светофор
    damage = State()      # повреждения / пострадавшие


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

    # Сводка
    full_description = (
        f"Место: {data.get('place')}\n"
        f"Движение: {data.get('movement')}\n"
        f"Знаки/светофор: {data.get('signs')}\n"
        f"Повреждения/пострадавшие: {data.get('damage')}\n"
    )

    # Анализ
    result = analyse_accident(full_description)

    # 1) Текстовый ответ в чат
    await message.answer(
        "✅ Спасибо, информация по ДТП собрана.\n\n"
        "📋 Сводка по описанию:\n"
        f"{full_description}\n"
        "⚖ Предварительный разбор:\n"
        f"{result}"
    )

    # 2) PDF-отчёт
    pdf_path = create_accident_pdf(full_description, result)
    pdf_file = FSInputFile(pdf_path)

    await message.answer_document(
        pdf_file,
        caption="📎 PDF-отчёт по ДТП (предварительный разбор)."
    )
