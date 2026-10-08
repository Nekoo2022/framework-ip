"""Вспомогательные функции консольного интерфейса."""

from __future__ import annotations

from datetime import date


class InputError(Exception):
    """Пользователь ввёл данные в неверном формате."""


def input_int(prompt: str) -> int:
    """Запросить целое число и сообщить об ошибке ввода."""
    raw = input(prompt)
    try:
        return int(raw)
    except ValueError as error:
        raise InputError("Нужно ввести целое число") from error


def input_date(prompt: str) -> date:
    """Запросить дату в формате ГГГГ-ММ-ДД."""
    raw = input(prompt).strip()
    try:
        return date.fromisoformat(raw)
    except ValueError as error:
        raise InputError("Дата указывается в формате ГГГГ-ММ-ДД") from error


def public_attributes(obj: object) -> dict[str, object]:
    """Вернуть публичные поля объекта средствами интроспекции."""
    return {
        name: value
        for name, value in vars(obj).items()
        if not name.startswith("_")
    }
