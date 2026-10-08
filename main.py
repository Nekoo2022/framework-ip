"""Консольный интерфейс сервиса бронирования репетиционных."""

from __future__ import annotations

from models.bookings import (
    BookingError,
    calculate_booking_price,
    cancel_booking,
    create_booking,
    find_booking_by_id,
    get_booking_status,
    is_room_available,
    show_bookings,
    show_room_info,
)
from models.musicians import find_musician_by_id, show_musicians
from models.rooms import (
    find_room,
    find_room_by_id,
    iter_suitable_rooms,
    show_rooms,
    sort_rooms_by_price,
)
from storage import (
    StorageError,
    load_bookings,
    load_musicians,
    load_rooms,
    save_bookings,
)
from utils import InputError, input_date, input_int, public_attributes


def _print_menu() -> None:
    """Показать команды приложения."""
    print()
    print("1. Список помещений")
    print("2. Информация о помещении")
    print("3. Проверить доступность")
    print("4. Рассчитать стоимость")
    print("5. Создать бронирование")
    print("6. Отменить бронирование")
    print("7. Список бронирований")
    print("8. Список музыкантов")
    print("0. Сохранить и выйти")


def _show_room_details(rooms: list, bookings: list) -> None:
    """Показать карточку помещения и статус на выбранную дату."""
    room_id = input_int("Идентификатор помещения: ")
    room = find_room_by_id(rooms, room_id)
    if room is None:
        print("Помещение не найдено.")
        return
    print(room)
    for name, value in public_attributes(room).items():
        print(f"  {name}: {value}")
    booking_date = input_date("Дата (ГГГГ-ММ-ДД): ")
    start_time = input("Время (ЧЧ:ММ): ").strip()
    hours = input_int("Часов: ")
    available = is_room_available(
        bookings,
        room,
        booking_date,
        start_time,
        hours,
    )
    print(get_booking_status(available))
    print(f"Стоимость: {room.price_for(hours)} руб.")


def run() -> None:
    """Запустить меню и работать с данными из JSON."""
    rooms = load_rooms()
    musicians = load_musicians()
    bookings = load_bookings(rooms=rooms, musicians=musicians)
    print("Сервис бронирования репетиционных помещений")
    while True:
        _print_menu()
        choice = input("Команда: ").strip()
        try:
            if choice == "1":
                show_rooms(sort_rooms_by_price(rooms))
            elif choice == "2":
                _show_room_details(rooms, bookings)
            elif choice == "3":
                query = input("Часть названия: ").strip()
                people = input_int("Размер группы: ")
                matched = find_room(rooms, query)
                suitable = list(iter_suitable_rooms(matched, people))
                show_rooms(suitable)
            elif choice == "4":
                booking_id = input_int("Идентификатор бронирования: ")
                booking = find_booking_by_id(bookings, booking_id)
                if booking is None:
                    print("Бронирование не найдено.")
                else:
                    show_room_info(booking)
                    print(get_booking_status(not booking.is_cancelled))
                    print(f"К оплате: {calculate_booking_price(booking)} руб.")
            elif choice == "5":
                show_rooms(rooms)
                show_musicians(musicians)
                room = find_room_by_id(rooms, input_int("Помещение: "))
                musician = find_musician_by_id(
                    musicians,
                    input_int("Музыкант: "),
                )
                if room is None or musician is None:
                    print("Помещение или музыкант не найдены.")
                    continue
                booking = create_booking(
                    bookings,
                    room,
                    musician,
                    input_date("Дата (ГГГГ-ММ-ДД): "),
                    input("Время (ЧЧ:ММ): ").strip(),
                    input_int("Часов: "),
                )
                print(booking)
                print(f"Стоимость: {booking.total_price} руб.")
            elif choice == "6":
                show_bookings(bookings)
                cancel_booking(bookings, input_int("Идентификатор: "))
                print("Бронирование отменено.")
            elif choice == "7":
                show_bookings(bookings)
            elif choice == "8":
                show_musicians(musicians)
            elif choice == "0":
                save_bookings(bookings)
                print("Данные сохранены.")
                break
            else:
                print("Нет такой команды.")
        except (InputError, BookingError, StorageError, ValueError) as error:
            print(f"Ошибка: {error}")


if __name__ == "__main__":
    try:
        run()
    except StorageError as error:
        print(f"Ошибка: {error}")
