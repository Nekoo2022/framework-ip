"""Общие данные шаблонов."""

from datetime import date


def project_info(request: object) -> dict[str, object]:
    """Передать в каждый шаблон название проекта и текущий год."""
    return {
        "project_name": "Сервис бронирования репетиционных помещений",
        "current_year": date.today().year,
    }
