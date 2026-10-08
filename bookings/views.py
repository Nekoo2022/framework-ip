"""Страницы бронирований."""

from django.shortcuts import render

from models.bookings import find_booking_by_id
from storage import load_project


def booking_list(request):
    """Показать бронирования из JSON-хранилища."""
    _rooms, _musicians, bookings = load_project()
    context = {"bookings": bookings}
    return render(request, "bookings/booking_list.html", context)


def booking_detail(request, booking_id: int):
    """Показать одно бронирование и связанные объекты."""
    _rooms, _musicians, bookings = load_project()
    booking = find_booking_by_id(bookings, booking_id)
    if booking is None:
        return render(
            request,
            "bookings/booking_not_found.html",
            status=404,
        )
    context = {"booking": booking}
    return render(request, "bookings/booking_detail.html", context)
