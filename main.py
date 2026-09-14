from datetime import datetime

musician_name = "Иван Петров"
room_name = "Репетиционная №2"
booking_time = "18:00"
booking_date = datetime(2026, 9, 20)

is_available = True
hours = 3
price_per_hour = 1200


def show_room_info():
    print("=== Информация о бронировании ===")
    print(f"Музыкант: {musician_name}")
    print(f"Помещение: {room_name}")
    print(f"Дата: {booking_date.date()}")
    print(f"Время: {booking_time}")


def check_availability():
    if is_available:
        return "Помещение доступно для бронирования."
    return "Помещение уже занято."


def calculate_booking_price():
    total = hours * price_per_hour
    return total


show_room_info()
print(check_availability())
print(f"Продолжительность: {hours} ч.")
print(f"Стоимость бронирования: {calculate_booking_price()} руб.")