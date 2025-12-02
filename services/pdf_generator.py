from pathlib import Path
from datetime import datetime
import sys

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader

# Шрифты (Windows)
FONT_PATH_REGULAR = Path(r"C:\Windows\Fonts\arial.ttf")
FONT_PATH_BOLD = Path(r"C:\Windows\Fonts\arialbd.ttf")

if not FONT_PATH_REGULAR.exists():
    print(f"[PDF] Не найден шрифт {FONT_PATH_REGULAR}", file=sys.stderr)
if not FONT_PATH_BOLD.exists():
    print(f"[PDF] Не найден шрифт {FONT_PATH_BOLD}", file=sys.stderr)

if FONT_PATH_REGULAR.exists():
    pdfmetrics.registerFont(TTFont("ZanAI-Regular", str(FONT_PATH_REGULAR)))
if FONT_PATH_BOLD.exists():
    pdfmetrics.registerFont(TTFont("ZanAI-Bold", str(FONT_PATH_BOLD)))

LOGO_PATH = Path(__file__).resolve().parent.parent / "branding" / "logo.png"


def create_accident_pdf(
    summary_text: str,
    analysis_text: str,
    scheme_text: str | None = None,
    actions_text: str | None = None,
) -> str:
    """
    Генерирует PDF-отчёт по ДТП и возвращает путь к файлу.

    summary_text  – сводка (место, движение, знаки, повреждения)
    analysis_text – юридический разбор
    scheme_text   – описательная схема ДТП (опционально)
    actions_text  – рекомендации по действиям (опционально)
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

    # Логотип
    if LOGO_PATH.exists():
        try:
            logo = ImageReader(str(LOGO_PATH))
            logo_width = 120
            lw, lh = logo.getSize()
            logo_height = logo_width * lh / lw
            logo_x = width - margin - logo_width
            logo_y = height - margin - logo_height
            c.drawImage(logo, logo_x, logo_y, width=logo_width, height=logo_height, mask="auto")
        except Exception as e:
            print(f"[PDF] Ошибка логотипа: {e}", file=sys.stderr)

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

    # Заголовок
    draw_multiline("Отчёт по ДТП (предварительный разбор)", y, bold=True, size=16)
    y -= 30

    # Дата
    c.setFont("ZanAI-Regular" if "ZanAI-Regular" in pdfmetrics.getRegisteredFontNames() else "Helvetica", 11)
    c.drawString(x, y, f"Дата формирования: {datetime.now().strftime('%d.%m.%Y %H:%M')}")
    y -= 30

    # Сводка
    draw_multiline("Сводка по описанию:", y, bold=True, size=13)
    y -= 20
    y = draw_multiline(summary_text, y - 5, bold=False, size=11)

    # Схема ДТП
    if scheme_text:
        y -= 20
        draw_multiline("Схема ДТП (описательная):", y, bold=True, size=13)
        y -= 20
        y = draw_multiline(scheme_text, y - 5, bold=False, size=11)

    # Анализ
    y -= 20
    draw_multiline("Предварительный юридический анализ:", y, bold=True, size=13)
    y -= 20
    y = draw_multiline(analysis_text, y - 5, bold=False, size=11)

    # Рекомендации
    if actions_text:
        y -= 20
        draw_multiline("Рекомендации по дальнейшим действиям:", y, bold=True, size=13)
        y -= 20
        y = draw_multiline(actions_text, y - 5, bold=False, size=11)

    # Штамп "КОНФИДЕНЦИАЛЬНО"
    stamp_text = "КОНФИДЕНЦИАЛЬНО"
    stamp_font = "ZanAI-Bold" if "ZanAI-Bold" in pdfmetrics.getRegisteredFontNames() else "Helvetica-Bold"
    stamp_size = 12

    c.setFont(stamp_font, stamp_size)
    text_width = c.stringWidth(stamp_text, stamp_font, stamp_size)
    stamp_x = (width - text_width) / 2
    stamp_y = margin / 2 + 5

    padding_x = 10
    padding_y = 6

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

    c.setFillColor(colors.red)
    c.drawString(stamp_x, stamp_y, stamp_text)

    c.setFillColor(colors.black)
    c.setStrokeColor(colors.black)

    c.showPage()
    c.save()

    return str(filepath)
