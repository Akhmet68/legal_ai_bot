from pathlib import Path
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def create_accident_pdf(summary_text: str, analysis_text: str) -> str:
    """
    Генерирует PDF-отчёт по ДТП и возвращает путь к файлу.
    """

    out_dir = Path(__file__).resolve().parent.parent / "pdf_reports"
    out_dir.mkdir(exist_ok=True)

    filename = f"accident_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    filepath = out_dir / filename

    c = canvas.Canvas(str(filepath), pagesize=A4)
    width, height = A4

    x = 40
    y = height - 50

    def draw_multiline(text: str, start_y: float) -> float:
        nonlocal c
        y_pos = start_y
        for line in text.split("\n"):
            if y_pos < 60:
                c.showPage()
                y_pos = height - 50
            c.drawString(x, y_pos, line)
            y_pos -= 16
        return y_pos

    c.setFont("Helvetica-Bold", 14)
    c.drawString(x, y, "Отчёт по ДТП (предварительный разбор)")
    y -= 30

    c.setFont("Helvetica", 11)
    c.drawString(x, y, f"Дата формирования: {datetime.now().strftime('%d.%m.%Y %H:%M')}")
    y -= 30

    c.setFont("Helvetica-Bold", 12)
    c.drawString(x, y, "Сводка по описанию:")
    y -= 20

    c.setFont("Helvetica", 11)
    y = draw_multiline(summary_text, y - 5)

    y -= 20
    c.setFont("Helvetica-Bold", 12)
    c.drawString(x, y, "Предварительный юридический анализ:")
    y -= 20

    c.setFont("Helvetica", 11)
    draw_multiline(analysis_text, y - 5)

    c.showPage()
    c.save()

    return str(filepath)
