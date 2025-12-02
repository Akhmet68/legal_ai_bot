from pathlib import Path

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"


def get_template_list() -> str:
    """
    Возвращает список доступных шаблонов в текстовом виде.
    """
    return (
        "1 — Договор купли-продажи (упрощённый)\n"
        "2 — Заявление в ГАИ о ДТП\n"
        "3 — Исковое заявление (общий шаблон)"
    )


def get_template_by_code(code: str) -> str | None:
    code = code.strip()

    filename_map = {
        "1": "dogovor_kuply.txt",
        "2": "zayavlenie_v_gai.txt",
        "3": "isk_obrazec.txt",
    }

    filename = filename_map.get(code)
    if not filename:
        return None

    path = TEMPLATES_DIR / filename

    if not path.exists():
        return "Шаблон пока не заполнен. В демо-версии можно показать здесь структуру документа."

    return path.read_text(encoding="utf-8")
