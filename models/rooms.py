"""Помещения репетиционной базы."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any


class Room:
    """Помещение, которое можно забронировать."""

    def __init__(
        self,
        room_id: int,
        name: str,
        capacity: int,
        price_per_hour: int,
    ) -> None:
        """Создать помещение и проверить числовые характеристики."""
        if capacity <= 0:
            raise ValueError("Вместимость должна быть положительной")
        if price_per_hour < 0:
            raise ValueError("Цена часа не может быть отрицательной")
        self.id = room_id
        self.name = name
        self.capacity = capacity
        self.price_per_hour = price_per_hour

    def is_suitable_for(self, people: int) -> bool:
        """Проверить, помещается ли группа указанного размера."""
        return 0 < people <= self.capacity

    def price_for(self, hours: int) -> int:
        """Рассчитать стоимость аренды на указанное число часов."""
        if hours <= 0:
            raise ValueError("Количество часов должно быть положительным")
        return self.price_per_hour * hours

    def to_dict(self) -> dict[str, Any]:
        """Преобразовать помещение в словарь для JSON."""
        return {
            "id": self.id,
            "name": self.name,
            "capacity": self.capacity,
            "price_per_hour": self.price_per_hour,
            "type": "room",
        }

    def __str__(self) -> str:
        """Вернуть краткое описание помещения."""
        return (
            f"{self.name} ({self.capacity} мест, "
            f"{self.price_per_hour} руб./ч)"
        )


class RehearsalRoom(Room):
    """Репетиционная: к аренде зала добавляется комплект оборудования."""

    def __init__(
        self,
        room_id: int,
        name: str,
        capacity: int,
        price_per_hour: int,
        equipment: list[str],
        equipment_fee: int = 0,
    ) -> None:
        """Создать репетиционную с перечнем оборудования."""
        super().__init__(room_id, name, capacity, price_per_hour)
        if equipment_fee < 0:
            raise ValueError(
                "Доплата за оборудование не может быть отрицательной"
            )
        self.equipment = equipment
        self.equipment_fee = equipment_fee

    def price_for(self, hours: int) -> int:
        """Посчитать аренду зала и почасовую доплату за оборудование."""
        if hours <= 0:
            raise ValueError("Количество часов должно быть положительным")
        hourly = self.price_per_hour + self.equipment_fee
        return hourly * hours

    def to_dict(self) -> dict[str, Any]:
        """Добавить к данным помещения оборудование и его доплату."""
        payload = super().to_dict()
        payload["type"] = "rehearsal"
        payload["equipment"] = list(self.equipment)
        payload["equipment_fee"] = self.equipment_fee
        return payload

    def __str__(self) -> str:
        """Вернуть описание репетиционной вместе с комплектом."""
        if self.equipment:
            equipment = ", ".join(self.equipment)
        else:
            equipment = "без комплекта"
        return f"{super().__str__()}; оборудование: {equipment}"


def room_from_dict(data: dict[str, Any]) -> Room:
    """Собрать помещение нужного класса из словаря JSON."""
    common = {
        "room_id": int(data["id"]),
        "name": str(data["name"]),
        "capacity": int(data["capacity"]),
        "price_per_hour": int(data["price_per_hour"]),
    }
    if data.get("type") == "rehearsal":
        equipment = data.get("equipment", [])
        if not isinstance(equipment, list):
            raise ValueError("Оборудование должно быть списком")
        return RehearsalRoom(
            equipment=[str(item) for item in equipment],
            equipment_fee=int(data.get("equipment_fee", 0)),
            **common,
        )
    return Room(**common)


def add_room(rooms: list[Room], room: Room) -> None:
    """Добавить помещение, если идентификатор ещё не занят."""
    if find_room_by_id(rooms, room.id) is not None:
        raise ValueError("Помещение с таким идентификатором уже есть")
    rooms.append(room)


def find_room_by_id(rooms: list[Room], room_id: int) -> Room | None:
    """Найти помещение по идентификатору."""
    for room in rooms:
        if room.id == room_id:
            return room
    return None


def find_room(rooms: list[Room], query: str) -> list[Room]:
    """Найти помещения, в названии которых есть подстрока."""
    needle = query.casefold()
    found: list[Room] = []
    for room in rooms:
        if needle in room.name.casefold():
            found.append(room)
    return found


def check_room_capacity(
    rooms: list[Room],
    room_id: int,
    min_capacity: int,
) -> bool:
    """Проверить, что помещение вмещает не меньше указанного числа людей."""
    room = find_room_by_id(rooms, room_id)
    if room is None:
        return False
    return room.capacity >= min_capacity


def filter_rooms_by_capacity(
    rooms: list[Room],
    min_capacity: int,
) -> list[Room]:
    """Отобрать помещения с вместимостью не ниже заданной."""
    return [room for room in rooms if room.capacity >= min_capacity]


def sort_rooms_by_price(rooms: list[Room]) -> list[Room]:
    """Отсортировать помещения по цене часа."""
    return sorted(rooms, key=lambda room: room.price_per_hour)


def iter_suitable_rooms(
    rooms: list[Room],
    people: int,
) -> Iterator[Room]:
    """Поочерёдно вернуть помещения, подходящие группе."""
    for room in rooms:
        if room.is_suitable_for(people):
            yield room


def show_rooms(rooms: list[Room]) -> None:
    """Вывести список помещений в консоль."""
    if not rooms:
        print("Помещения не найдены.")
        return
    for room in rooms:
        print(room)
