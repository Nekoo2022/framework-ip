"""Главная страница и общая ошибка 404."""

from django.shortcuts import render

from storage import load_project


def index(request):
    """Показать описание сервиса и переход к разделам."""
    rooms, musicians, bookings = load_project()
    context = {
        "rooms_count": len(rooms),
        "musicians_count": len(musicians),
        "bookings_count": len(bookings),
    }
    return render(request, "homepage/index.html", context)


def page_not_found(request, exception):
    """Показать страницу для адреса, которого нет в маршрутах."""
    return render(
        request,
        "404.html",
        status=404,
    )
