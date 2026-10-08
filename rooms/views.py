"""Страницы помещений."""

from datetime import date

from django.shortcuts import render

from models.bookings import get_booking_status, is_room_available
from models.rooms import find_room_by_id
from storage import load_project


def room_list(request):
    """Показать помещения из JSON-хранилища."""
    rooms, _musicians, _bookings = load_project()
    context = {"rooms": rooms}
    return render(request, "rooms/room_list.html", context)


def room_detail(request, room_id: int):
    """Показать помещение и доступность на текущую дату."""
    rooms, _musicians, bookings = load_project()
    room = find_room_by_id(rooms, room_id)
    if room is None:
        return render(
            request,
            "rooms/room_not_found.html",
            status=404,
        )
    today = date.today()
    available = is_room_available(bookings, room, today)
    context = {
        "room": room,
        "available": available,
        "today": today,
        "status_text": get_booking_status(available),
        "hour_price": room.price_for(1),
    }
    return render(request, "rooms/room_detail.html", context)
