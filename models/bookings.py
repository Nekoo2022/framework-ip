"""Бронирования репетиционных помещений."""

from __future__ import annotations

from datetime import date
from typing import Any

from models.exceptions import BookingError
from models.musicians import Musician, find_musician_by_id
from models.rooms import Room, find_room_by_id


def _minutes(value: str) -> int:
    """Перевести время ЧЧ:ММ в минуты от начала суток."""
    parts = value.split(":")
    if len(parts) != 2:
        raise BookingError("Время указывается в формате ЧЧ:ММ")
    try:
        hours = int(parts[0])
        minutes = int(parts[1])
    except ValueError as error:
        raise BookingError("Время указывается в формате ЧЧ:ММ") from error
    if hours < 0 or hours > 23 or minutes < 0 or minutes > 59:
        raise BookingError("Некорректное время")
    return hours * 60 + minutes


def _intervals_overlap(
    start_time: str,
    hours: int,
    other_start: str,
    other_hours: int,
) -> bool:
    """Проверить пересечение двух интервалов в один день."""
    start = _minutes(start_time)
    end = start + hours * 60
    other_begin = _minutes(other_start)
    other_end = other_begin + other_hours * 60
    return start < other_end and other_begin < end


class Booking:
    """Бронирование помещения музыкантом на дату и время."""

    def __init__(
        self,
        booking_id: int,
        room: Room,
        musician: Musician,
        booking_date: date,
        start_time: str,
        hours: int,
        is_cancelled: bool = False,
    ) -> None:
        """Создать бронирование и связать помещение с музыкантом."""
        if hours <= 0:
            raise ValueError("Продолжительность должна быть положительной")
        _minutes(start_time)
        self.id = booking_id
        self.room = room
        self.musician = musician
        self.booking_date = booking_date
        self.start_time = start_time
        self.hours = hours
        self.is_cancelled = is_cancelled

    @property
    def status(self) -> str:
        """Вернуть текстовый статус без вызова метода."""
        if self.is_cancelled:
            return "отменено"
        return "активно"

    @property
    def total_price(self) -> int:
        """Стоимость с учётом класса помещения."""
        return self.room.price_for(self.hours)

    def cancel(self) -> None:
        """Отменить бронирование."""
        self.is_cancelled = True

    def overlaps(self, other: Booking) -> bool:
        """Проверить, пересекается ли бронь с другой по залу и времени."""
        if self.is_cancelled or other.is_cancelled:
            return False
        if self.room.id != other.room.id:
            return False
        if self.booking_date != other.booking_date:
            return False
        return _intervals_overlap(
            self.start_time,
            self.hours,
            other.start_time,
            other.hours,
        )

    def to_dict(self) -> dict[str, Any]:
        """Преобразовать бронирование в словарь для JSON."""
        return {
            "id": self.id,
            "room_id": self.room.id,
            "musician_id": self.musician.id,
            "date": self.booking_date.isoformat(),
            "start_time": self.start_time,
            "hours": self.hours,
            "is_cancelled": self.is_cancelled,
        }

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
        rooms: list[Room],
        musicians: list[Musician],
    ) -> Booking:
        """Собрать бронирование и подставить связанные объекты."""
        room = find_room_by_id(rooms, int(data["room_id"]))
        musician = find_musician_by_id(musicians, int(data["musician_id"]))
        if room is None or musician is None:
            raise ValueError("Связанные помещение или музыкант не найдены")
        return cls(
            booking_id=int(data["id"]),
            room=room,
            musician=musician,
            booking_date=date.fromisoformat(str(data["date"])),
            start_time=str(data["start_time"]),
            hours=int(data["hours"]),
            is_cancelled=bool(data.get("is_cancelled", False)),
        )

    def __str__(self) -> str:
        """Вернуть краткую строку бронирования."""
        return (
            f"Бронирование #{self.id}: {self.room.name}, "
            f"{self.musician.name}, {self.booking_date.isoformat()} "
            f"{self.start_time}, {self.hours} ч., {self.status}"
        )


def get_booking_status(is_available: bool) -> str:
    """Вернуть текст доступности помещения.

    Функция сохранена из начального сценария первой практической работы.
    """
    if is_available:
        return "Помещение доступно для бронирования."
    return "Помещение уже занято."


def calculate_booking_price(booking: Booking) -> int:
    """Рассчитать стоимость бронирования."""
    return booking.total_price


def is_room_available(
    bookings: list[Booking],
    room: Room,
    booking_date: date,
    start_time: str | None = None,
    hours: int | None = None,
) -> bool:
    """Проверить, свободно ли помещение на дату и, при необходимости, время."""
    for item in bookings:
        if item.is_cancelled or item.room.id != room.id:
            continue
        if item.booking_date != booking_date:
            continue
        if start_time is None or hours is None:
            return False
        if _intervals_overlap(start_time, hours, item.start_time, item.hours):
            return False
    return True


def create_booking(
    bookings: list[Booking],
    room: Room,
    musician: Musician,
    booking_date: date,
    start_time: str,
    hours: int,
) -> Booking:
    """Создать бронирование, если выбранный интервал свободен."""
    if not is_room_available(
        bookings,
        room,
        booking_date,
        start_time,
        hours,
    ):
        raise BookingError("Помещение уже занято на выбранное время")
    next_id = 1
    if bookings:
        next_id = max(item.id for item in bookings) + 1
    booking = Booking(
        booking_id=next_id,
        room=room,
        musician=musician,
        booking_date=booking_date,
        start_time=start_time,
        hours=hours,
    )
    bookings.append(booking)
    return booking


def cancel_booking(bookings: list[Booking], booking_id: int) -> Booking:
    """Отменить бронирование по идентификатору."""
    booking = find_booking_by_id(bookings, booking_id)
    if booking is None:
        raise BookingError("Бронирование не найдено")
    booking.cancel()
    return booking


def find_booking_by_id(
    bookings: list[Booking],
    booking_id: int,
) -> Booking | None:
    """Найти бронирование по идентификатору."""
    for booking in bookings:
        if booking.id == booking_id:
            return booking
    return None


def show_bookings(bookings: list[Booking]) -> None:
    """Вывести список бронирований в консоль."""
    if not bookings:
        print("Бронирования не найдены.")
        return
    for booking in bookings:
        print(booking)


def show_room_info(booking: Booking) -> None:
    """Показать сценарий просмотра информации о бронировании."""
    print("=== Информация о бронировании ===")
    print(f"Музыкант: {booking.musician.name}")
    print(f"Помещение: {booking.room.name}")
    print(f"Дата: {booking.booking_date.isoformat()}")
    print(f"Время: {booking.start_time}")
    print(f"Продолжительность: {booking.hours} ч.")
    print(f"Стоимость бронирования: {calculate_booking_price(booking)} руб.")
