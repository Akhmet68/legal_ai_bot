from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

router = Router()

# Главное меню
main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="💬 Задать вопрос"),
            KeyboardButton(text="📄 Документ"),
        ],
        [
            KeyboardButton(text="🚗 ДТП"),
            KeyboardButton(text="📑 Шаблоны"),
        ],
        [
            KeyboardButton(text="👤 Клиент"),
        ],
    ],
    resize_keyboard=True
)


@router.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        "👋 Привет! Я юридический AI-помощник ZanAI.\n\n"
        "Я могу:\n"
        "• Ответить на юридический вопрос\n"
        "• Проанализировать документ (PDF/фото)\n"
        "• Подсказать по ситуации с ДТП\n"
        "• Выдать шаблон договора / заявления\n"
        "• Сохранить данные клиента в карточку\n\n"
        "Выберите действие через кнопки ниже или используйте команды (/help).",
        reply_markup=main_kb
    )


# Обработка кнопок главного меню

@router.message(lambda m: m.text == "💬 Задать вопрос")
async def btn_question(message: types.Message):
    await message.answer(
        "Напишите ваш юридический вопрос в формате:\n"
        "<code>/question Ваш вопрос...</code>\n\n"
        "Например:\n"
        "<code>/question Как разделить имущество после развода?</code>"
    )


@router.message(lambda m: m.text == "📄 Документ")
async def btn_document(message: types.Message):
    await message.answer(
        "Отправьте PDF-файл или фото документа.\n"
        "Также можете использовать команду:\n"
        "<code>/document</code>"
    )


@router.message(lambda m: m.text == "🚗 ДТП")
async def btn_accident(message: types.Message):
    await message.answer(
        "Я задам несколько вопросов по ДТП и дам предварительный разбор.\n"
        "Нажмите:\n"
        "<code>/accident</code>"
    )


@router.message(lambda m: m.text == "📑 Шаблоны")
async def btn_templates(message: types.Message):
    await message.answer(
        "Чтобы получить список шаблонов, используйте:\n"
        "<code>/template</code>\n"
        "Например: <code>/template 1</code>"
    )


@router.message(lambda m: m.text == "👤 Клиент")
async def btn_client(message: types.Message):
    await message.answer(
        "Создание карточки клиента.\n\n"
        "Формат:\n"
        "<code>/client Имя Телефон Комментарий</code>\n\n"
        "Пример:\n"
        "<code>/client Иван 87771234567 ДТП на перекрёстке, нужна помощь</code>"
    )
