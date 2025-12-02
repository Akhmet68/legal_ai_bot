from pathlib import Path
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader


# Пути к шрифтам с кириллицей (Windows)
FONT_PATH_REGULAR = r"C:\Windows\Fonts\arial.ttf"
FONT_PATH_BOLD = r"C:\Windows\Fonts\arialbd.ttf"

# Путь к логотипу ZanAI
LOGO_PATH = Path(__file__).resolve().parent.parent / "branding" / "logo.png"

# Регистрируем шрифты
try:
    pdfmetrics.registerFont(TTFont("Arial",      FONT_PATH_REGULAR))
    pdfmetrics.registerFont(TTFont("Arial-Bold", FONT_PATH_BOLD))
except Exception:
    # Если шрифты не найдены, reportlab всё равно не упадёт
    pass


def create_accident_pdf(summary_text: str, analysis_text: str) -> str:
    """
    Генерирует PDF-отчёт по ДТП и возвращает путь к файлу.
    Вверху — логотип ZanAI, внизу — штамп «КОНФИДЕНЦИАЛЬНО».
    """

    out_dir = Path(__file__).resolve().parent.parent / "pdf_reports"
    out_dir.mkdir(exist_ok=True)

    filename = f"accident_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    filepath = out_dir / filename

    c = canvas.Canvas(str(filepath), pagesize=A4)
    width, height = A4

    margin = 40
    x = margin
    y = height - margin

    # --- ЛОГОТИП ВВЕРХУ ---
    if LOGO_PATH.exists():
        try:
            logo = ImageReader(str(LOGO_PATH))
            logo_width = 120  # ширина логотипа в pt
            lw, lh = logo.getSize()
            logo_height = logo_width * lh / lw

            # Рисуем в правом верхнем углу
            logo_x = width - margin - logo_width
            logo_y = height - margin - logo_height

            c.drawImage(
                logo,
                logo_x,
                logo_y,
                width=logo_width,
                height=logo_height,
                mask='auto'
            )
        except Exception:
            # если с логотипом что-то не так — просто пропускаем
            pass

    def draw_multiline(text: str, start_y: float, font_name: str = "Arial", font_size: int = 11) -> float:
        nonlocal c
        c.setFont(font_name, font_size)
        y_pos = start_y
        for line in text.split("\n"):
            if y_pos < 60:
                c.showPage()
                y_pos = height - margin
                c.setFont(font_name, font_size)
            c.drawString(x, y_pos, line)
            y_pos -= 16
        return y_pos

    # --- Заголовок ---
    c.setFont("Arial-Bold", 16)
    c.drawString(x, y, "Отчёт по ДТП (предварительный разбор)")
    y -= 30

    # --- Дата ---
    c.setFont("Arial", 11)
    c.drawString(x, y, f"Дата формирования: {datetime.now().strftime('%d.%m.%Y %H:%M')}")
    y -= 30

    # --- Сводка ---
    c.setFont("Arial-Bold", 13)
    c.drawString(x, y, "Сводка по описанию:")
    y -= 20

    y = draw_multiline(summary_text, y - 5)

    # --- Анализ ---
    y -= 20
    c.setFont("Arial-Bold", 13)
    c.drawString(x, y, "Предварительный юридический анализ:")
    y -= 20

    draw_multiline(analysis_text, y - 5)

    # --- ШТАМП «КОНФИДЕНЦИАЛЬНО» ВНИЗУ ---
    stamp_text = "КОНФИДЕНЦИАЛЬНО"
    stamp_font = "Arial-Bold"
    stamp_size = 12

    c.setFont(stamp_font, stamp_size)
    text_width = c.stringWidth(stamp_text, stamp_font, stamp_size)

    # Позиция по центру внизу
    stamp_x = (width - text_width) / 2
    stamp_y = margin / 2 + 5

    padding_x = 10
    padding_y = 6

    # Рисуем рамку
    c.setStrokeColor(colors.red)
    c.setFillColor(colors.white)
    c.roundRect(
        stamp_x - padding_x,
        stamp_y - padding_y,
        text_width + padding_x * 2,
        stamp_y + padding_y,
        6,
        stroke=1,
        fill=1,
    )

    # Сам текст штампа
    c.setFillColor(colors.red)
    c.drawString(stamp_x, stamp_y, stamp_text)

    # На всякий случай возвращаем чёрный цвет по умолчанию
    c.setFillColor(colors.black)
    c.setStrokeColor(colors.black)

    c.showPage()
    c.save()

    return str(filepath)
