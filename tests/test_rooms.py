"""Тесты работы с помещениями."""

from models.rooms import (
    RehearsalRoom,
    Room,
    add_room,
    check_room_capacity,
    find_room,
    room_from_dict,
)


def test_add_room() -> None:
    """Добавление помещения увеличивает коллекцию."""
    rooms: list[Room] = []
    add_room(rooms, Room(1, "Репетиционная №2", 6, 1200))
    assert len(rooms) == 1


def test_find_room() -> None:
    """Поиск по части названия не зависит от регистра."""
    rooms = [Room(1, "Репетиционная №2", 6, 1200)]
    assert find_room(rooms, "репетиционная")


def test_check_room_capacity() -> None:
    """Помещение подходит, если вместимость не ниже запрошенной."""
    rooms = [Room(1, "Зал со звуком", 8, 1800)]
    assert check_room_capacity(rooms, 1, 5)
    assert not check_room_capacity(rooms, 1, 10)


def test_rehearsal_room_adds_equipment_fee() -> None:
    """Доплата за оборудование меняет расчёт стоимости наследника."""
    plain = Room(1, "Зал", 4, 1000)
    equipped = RehearsalRoom(
        2,
        "Репетиционная №1",
        4,
        900,
        ["микрофон"],
        equipment_fee=200,
    )
    assert plain.price_for(2) == 2000
    assert equipped.price_for(2) == 2200


def test_room_from_dict_builds_rehearsal_room() -> None:
    """JSON с типом rehearsal создаёт объект наследника."""
    room = room_from_dict(
        {
            "id": 2,
            "name": "Репетиционная №2",
            "capacity": 6,
            "price_per_hour": 1200,
            "type": "rehearsal",
            "equipment": ["барабаны"],
            "equipment_fee": 0,
        }
    )
    assert isinstance(room, RehearsalRoom)
    assert room.price_for(3) == 3600
