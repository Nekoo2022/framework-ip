"""Корневые маршруты Django-проекта."""

from django.urls import include, path

urlpatterns = [
    path("", include("homepage.urls")),
    path("rooms/", include("rooms.urls")),
    path("bookings/", include("bookings.urls")),
]

handler404 = "homepage.views.page_not_found"
