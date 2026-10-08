"""Сохранение и загрузка данных проекта в JSON."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from models.bookings import Booking
from models.musicians import Musician
from models.rooms import Room, room_from_dict

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
ROOMS_PATH = DATA_DIR / "rooms.json"
MUSICIANS_PATH = DATA_DIR / "musicians.json"
BOOKINGS_PATH = DATA_DIR / "bookings.json"


class StorageError(Exception):
    """Ошибка чтения или записи файла данных."""


def _read_json(path: str | Path) -> Any:
    """Прочитать JSON через контекстный менеджер."""
    try:
        with open(path, encoding="utf-8") as source:
            return json.load(source)
    except FileNotFoundError as error:
        raise StorageError(f"Файл не найден: {path}") from error
    except json.JSONDecodeError as error:
        raise StorageError(f"Повреждён файл данных: {path}") from error


def _write_json(path: str | Path, payload: Any) -> None:
    """Записать JSON через контекстный менеджер."""
    try:
        with open(path, "w", encoding="utf-8") as target:
            json.dump(payload, target, ensure_ascii=False, indent=2)
            target.write("\n")
    except OSError as error:
        raise StorageError(f"Не удалось сохранить файл: {path}") from error


def load_rooms(path: str | Path = ROOMS_PATH) -> list[Room]:
    """Загрузить помещения из JSON и создать объекты."""
    raw = _read_json(path)
    if not isinstance(raw, list):
        raise StorageError("Ожидался список помещений")
    return [room_from_dict(item) for item in raw]


def save_rooms(rooms: list[Room], path: str | Path = ROOMS_PATH) -> None:
    """Сохранить помещения в JSON."""
    _write_json(path, [room.to_dict() for room in rooms])


def load_musicians(path: str | Path = MUSICIANS_PATH) -> list[Musician]:
    """Загрузить музыкантов из JSON и создать объекты."""
    raw = _read_json(path)
    if not isinstance(raw, list):
        raise StorageError("Ожидался список музыкантов")
    return [Musician.from_dict(item) for item in raw]


def save_musicians(
    musicians: list[Musician],
    path: str | Path = MUSICIANS_PATH,
) -> None:
    """Сохранить музыкантов в JSON."""
    _write_json(path, [musician.to_dict() for musician in musicians])


def load_bookings(
    path: str | Path = BOOKINGS_PATH,
    rooms: list[Room] | None = None,
    musicians: list[Musician] | None = None,
) -> list[Booking]:
    """Загрузить бронирования и связать их с помещениями и музыкантами."""
    raw = _read_json(path)
    if not isinstance(raw, list):
        raise StorageError("Ожидался список бронирований")
    room_list = load_rooms() if rooms is None else rooms
    musician_list = load_musicians() if musicians is None else musicians
    return [
        Booking.from_dict(item, room_list, musician_list)
        for item in raw
    ]


def load_project() -> tuple[list[Room], list[Musician], list[Booking]]:
    """Загрузить помещения, музыкантов и связанные бронирования."""
    rooms = load_rooms()
    musicians = load_musicians()
    bookings = load_bookings(rooms=rooms, musicians=musicians)
    return rooms, musicians, bookings


def save_bookings(
    bookings: list[Booking],
    path: str | Path = BOOKINGS_PATH,
) -> None:
    """Сохранить бронирования в JSON."""
    _write_json(path, [booking.to_dict() for booking in bookings])
