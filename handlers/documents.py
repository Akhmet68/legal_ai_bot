from aiogram import Router, types
from aiogram.filters import Command
from aiogram import F

from services.pdf_reader import read_pdf_stub
from services.ocr_reader import read_image_stub

router = Router()


@router.message(Command("document"))
async def cmd_document(message: types.Message):
    await message.answer(
        "Отправьте мне PDF-файл или фото документа, и я сделаю предварительный анализ.\n\n"
        "Сейчас работает демонстрационная версия анализа."
    )


@router.message(F.document)
async def handle_document(message: types.Message):
    doc = message.document

    if not doc.file_name.lower().endswith(".pdf"):
        await message.answer("Пока я работаю только с PDF-файлами как документами. Попробуйте отправить PDF или фото.")
        return

    await message.answer("📄 Документ получен. Выполняю предварительный анализ (демо)...")

    text_preview = read_pdf_stub(doc.file_name)

    await message.answer(
        "Результат (демо):\n\n"
        f"{text_preview}\n\n"
        "В полноценной версии здесь будет распознавание текста и проверка важных юридических пунктов."
    )


@router.message(F.photo)
async def handle_photo(message: types.Message):
    await message.answer("🖼 Фото документа получено. Выполняю предварительный анализ (демо)...")

    text_preview = read_image_stub()

    await message.answer(
        "Результат (демо):\n\n"
        f"{text_preview}\n\n"
        "В полноценной версии здесь будет OCR-распознавание текста по фото и юридический анализ."
    )
