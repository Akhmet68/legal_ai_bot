from pathlib import Path
from datetime import datetime
import sys

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader

# --- НАСТРОЙКИ ШРИФТА ---

# Попытка использовать Arial (Windows)
FONT_PATH_REGULAR = Path(r"C:\Windows\Fonts\Arial.ttf")
FONT_PATH_BOLD = Path(r"C:\Windows\Fonts\arialbd.ttf")

# Если Arial нет, можно заменить на любой другой TTF из C:\Windows\Fonts
# например:
# FONT_PATH_REGULAR = Path(r"C:\Windows\Fonts\segoeui.ttf")
# FONT_PATH_BOLD    = Path(r"C:\Windows\Fonts\segoeuib.ttf")

if not FONT_PATH_REGULAR.exists():
    print(f"[PDF] Не найден шрифт {FONT_PATH_REGULAR}", file=sys.stderr)
if not FONT_PATH_BOLD.exists():
    print(f"[PDF] Не найден шрифт {FONT_PATH_BOLD}", file=sys.stderr)

# Регистрируем шрифты, если файлы существуют
if FONT_PATH_REGULAR.exists():
    pdfmetrics.registerFont(TTFont("ZanAI-Regular", str(FONT_PATH_REGULAR)))
else:
    # fallback – всё равно будет латиница и квадраты, но не упадёт
    print("[PDF] Используется базовый шрифт ReportLab (без кириллицы)", file=sys.stderr)

if FONT_PATH_BOLD.exists():
    pdfmetrics.registerFont(TTFont("ZanAI-Bold", str(FONT_PATH_BOLD)))
else:
    print("[PDF] Не удалось зарегистрировать жирный шрифт ZanAI-Bold", file=sys.stderr)


# --- ЛОГОТИП ---

LOGO_PATH = Path(__file__).resolve().parent.parent / "branding" / "logo.png"


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

    # --- ЛОГОТИП ВВЕРХУ СПРАВА ---
    if LOGO_PATH.exists():
        try:
            logo = ImageReader(str(LOGO_PATH))
            logo_width = 120
            lw, lh = logo.getSize()
            logo_height = logo_width * lh / lw

            logo_x = width - margin - logo_width
            logo_y = height - margin - logo_height

            c.drawImage(
                logo,
                logo_x,
                logo_y,
                width=logo_width,
                height=logo_height,
                mask="auto",
            )
        except Exception as e:
            print(f"[PDF] Ошибка при рисовании логотипа: {e}", file=sys.stderr)

    def draw_multiline(text: str, start_y: float, bold: bool = False, size: int = 11) -> float:
        nonlocal c
        font_name = "ZanAI-Bold" if bold and "ZanAI-Bold" in pdfmetrics.getRegisteredFontNames() \
            else "ZanAI-Regular" if "ZanAI-Regular" in pdfmetrics.getRegisteredFontNames() \
            else "Helvetica"

        c.setFont(font_name, size)
        y_pos = start_y
        for line in text.split("\n"):
            if y_pos < 60:
                c.showPage()
                y_pos = height - margin
                c.setFont(font_name, size)
            c.drawString(x, y_pos, line)
            y_pos -= 16
        return y_pos

    # --- Заголовок ---
    draw_multiline("Отчёт по ДТП (предварительный разбор)", y, bold=True, size=16)
    y -= 30

    # --- Дата ---
    c.setFont("ZanAI-Regular" if "ZanAI-Regular" in pdfmetrics.getRegisteredFontNames() else "Helvetica", 11)
    c.drawString(x, y, f"Дата формирования: {datetime.now().strftime('%d.%m.%Y %H:%M')}")
    y -= 30

    # --- Сводка ---
    draw_multiline("Сводка по описанию:", y, bold=True, size=13)
    y -= 20

    y = draw_multiline(summary_text, y - 5, bold=False, size=11)

    # --- Анализ ---
    y -= 20
    draw_multiline("Предварительный юридический анализ:", y, bold=True, size=13)
    y -= 20

    draw_multiline(analysis_text, y - 5, bold=False, size=11)

    # --- ШТАМП «КОНФИДЕНЦИАЛЬНО» ВНИЗУ ---
    stamp_text = "КОНФИДЕНЦИАЛЬНО"
    stamp_font = "ZanAI-Bold" if "ZanAI-Bold" in pdfmetrics.getRegisteredFontNames() else "Helvetica-Bold"
    stamp_size = 12

    c.setFont(stamp_font, stamp_size)
    text_width = c.stringWidth(stamp_text, stamp_font, stamp_size)

    stamp_x = (width - text_width) / 2
    stamp_y = margin / 2 + 5

    padding_x = 10
    padding_y = 6

    # Рамка
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

    # Текст штампа
    c.setFillColor(colors.red)
    c.drawString(stamp_x, stamp_y, stamp_text)

    # Возвращаем цвета по умолчанию
    c.setFillColor(colors.black)
    c.setStrokeColor(colors.black)

    c.showPage()
    c.save()

    return str(filepath)
