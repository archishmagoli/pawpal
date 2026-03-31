from datetime import date
from dataclasses import dataclass, field


@dataclass
class Pet:
    name: str
    age: int
    species: str
    tasks: list["Task"] = field(default_factory=list)

    def add_task(self, task: "Task") -> None:
        pass

    def remove_task(self, name: str) -> None:
        pass

    def get_tasks(self) -> list["Task"]:
        pass


@dataclass
class Task:
    name: str
    duration: int
    priority: str
    category: str
    start_time: str | None = None


@dataclass
class Owner:
    name: str
    available_time: int
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        pass

    def remove_pet(self, name: str) -> None:
        pass

    def get_pet(self, name: str) -> Pet | None:
        pass


@dataclass
class Schedule:
    date: date
    pet: Pet
    available_time: int
    tasks: list[Task] = field(default_factory=list)

    def generate_plan(self) -> None:
        pass

    def display_plan(self) -> None:
        pass
