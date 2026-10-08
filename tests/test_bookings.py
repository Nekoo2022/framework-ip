"""Тесты бронирования."""

from datetime import date

from models.bookings import (
    BookingError,
    calculate_booking_price,
    create_booking,
    get_booking_status,
    is_room_available,
)
from models.musicians import Musician
from models.rooms import RehearsalRoom


def _room() -> RehearsalRoom:
    """Помещение из начального сценария проекта."""
    return RehearsalRoom(
        2,
        "Репетиционная №2",
        6,
        1200,
        ["барабанная установка"],
        equipment_fee=0,
    )


def _musician() -> Musician:
    """Музыкант из начального сценария проекта."""
    return Musician(1, "Иван Петров", "гитара", "+7 900 111-22-33")


def test_is_room_available() -> None:
    """Пустой список бронирований означает свободное помещение."""
    assert is_room_available([], _room(), date(2026, 9, 20), "18:00", 3)


def test_duplicate_booking_forbidden() -> None:
    """Повторное бронирование того же интервала запрещено."""
    bookings = []
    room = _room()
    create_booking(
        bookings,
        room,
        _musician(),
        date(2026, 9, 20),
        "18:00",
        3,
    )
    assert not is_room_available(bookings, room, date(2026, 9, 20), "19:00", 1)


def test_cancelled_booking_frees_room() -> None:
    """Отменённая бронь не занимает помещение."""
    bookings = []
    room = _room()
    booking = create_booking(
        bookings,
        room,
        _musician(),
        date(2026, 9, 20),
        "18:00",
        3,
    )
    booking.cancel()
    assert is_room_available(bookings, room, date(2026, 9, 20), "18:00", 3)
    assert booking.status == "отменено"


def test_calculate_booking_price() -> None:
    """Три часа по 1200 рублей дают стоимость начального сценария."""
    booking = create_booking(
        [],
        _room(),
        _musician(),
        date(2026, 9, 20),
        "18:00",
        3,
    )
    assert calculate_booking_price(booking) == 3600
    assert get_booking_status(True).startswith("Помещение доступно")


def test_create_booking_rejects_overlap() -> None:
    """Создание пересекающейся брони завершается ошибкой."""
    bookings = []
    room = _room()
    create_booking(
        bookings,
        room,
        _musician(),
        date(2026, 9, 20),
        "18:00",
        3,
    )
    try:
        create_booking(
            bookings,
            room,
            _musician(),
            date(2026, 9, 20),
            "20:00",
            1,
        )
    except BookingError:
        assert len(bookings) == 1
    else:
        raise AssertionError("пересечение должно быть отклонено")
