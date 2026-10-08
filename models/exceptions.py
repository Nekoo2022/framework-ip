"""Исключения предметной области."""


class DomainError(Exception):
    """Базовая ошибка операций сервиса."""


class BookingError(DomainError):
    """Операцию с бронированием выполнить нельзя."""
