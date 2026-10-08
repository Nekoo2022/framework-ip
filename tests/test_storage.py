"""Тесты музыкантов и хранилища."""

from pathlib import Path

from models.musicians import Musician, add_musician
from storage import StorageError, load_bookings, load_rooms, save_rooms


def test_add_musician() -> None:
    """Музыкант добавляется в коллекцию."""
    musicians = []
    add_musician(musicians, Musician(1, "Иван Петров", "гитара", "123"))
    assert musicians[0].name == "Иван Петров"


def test_json_roundtrip(tmp_path: Path) -> None:
    """Объекты помещений сохраняются и снова загружаются из JSON."""
    from models.rooms import RehearsalRoom

    path = tmp_path / "rooms.json"
    original = [
        RehearsalRoom(2, "Репетиционная №2", 6, 1200, ["барабаны"], 0),
    ]
    save_rooms(original, path)
    loaded = load_rooms(path)
    assert loaded[0].name == "Репетиционная №2"
    assert loaded[0].price_for(3) == 3600


def test_missing_file_raises_storage_error(tmp_path: Path) -> None:
    """Отсутствующий файл не роняет программу необработанным исключением."""
    try:
        load_rooms(tmp_path / "missing.json")
    except StorageError as error:
        assert "не найден" in str(error)
    else:
        raise AssertionError("ожидалась StorageError")


def test_project_data_loads() -> None:
    """Рабочие JSON-файлы проекта собираются в связанные объекты."""
    rooms = load_rooms()
    bookings = load_bookings(rooms=rooms)
    assert len(rooms) >= 3
    assert bookings[0].musician.name == "Иван Петров"
    assert bookings[0].room.name == "Репетиционная №2"
