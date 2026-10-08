"""Музыканты, которые бронируют репетиционные."""

from __future__ import annotations

from typing import Any


class Musician:
    """Музыкант или представитель группы."""

    def __init__(
        self,
        musician_id: int,
        name: str,
        instrument: str,
        phone: str,
    ) -> None:
        """Создать музыканта."""
        if not name.strip():
            raise ValueError("Имя музыканта не может быть пустым")
        self.id = musician_id
        self.name = name.strip()
        self.instrument = instrument.strip()
        self.phone = phone.strip()

    def to_dict(self) -> dict[str, Any]:
        """Преобразовать музыканта в словарь для JSON."""
        return {
            "id": self.id,
            "name": self.name,
            "instrument": self.instrument,
            "phone": self.phone,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Musician:
        """Собрать музыканта из словаря JSON."""
        return cls(
            musician_id=int(data["id"]),
            name=str(data["name"]),
            instrument=str(data.get("instrument", "")),
            phone=str(data.get("phone", "")),
        )

    def __str__(self) -> str:
        """Вернуть имя и инструмент."""
        if self.instrument:
            return f"{self.name}, {self.instrument}"
        return self.name


def add_musician(musicians: list[Musician], musician: Musician) -> None:
    """Добавить музыканта, если идентификатор ещё не занят."""
    if find_musician_by_id(musicians, musician.id) is not None:
        raise ValueError("Музыкант с таким идентификатором уже есть")
    musicians.append(musician)


def find_musician_by_id(
    musicians: list[Musician],
    musician_id: int,
) -> Musician | None:
    """Найти музыканта по идентификатору."""
    for musician in musicians:
        if musician.id == musician_id:
            return musician
    return None


def show_musicians(musicians: list[Musician]) -> None:
    """Вывести список музыкантов в консоль."""
    if not musicians:
        print("Музыканты не найдены.")
        return
    for musician in musicians:
        print(f"{musician.id}. {musician}")
