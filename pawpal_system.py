from datetime import date
from dataclasses import dataclass, field


@dataclass
class Task:
    name: str
    duration: int       # minutes
    priority: str       # "high", "medium", "low"
    category: str
    start_time: str | None = None
    completed: bool = False


@dataclass
class Pet:
    name: str
    age: int
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def remove_task(self, name: str) -> None:
        self.tasks = [t for t in self.tasks if t.name != name]

    def get_tasks(self) -> list[Task]:
        return list(self.tasks)


@dataclass
class Owner:
    name: str
    available_time: int     # total minutes available per day
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        self.pets.append(pet)

    def remove_pet(self, name: str) -> None:
        self.pets = [p for p in self.pets if p.name != name]

    def get_pet(self, name: str) -> Pet | None:
        return next((p for p in self.pets if p.name == name), None)


@dataclass
class Schedule:
    """Per-pet daily schedule. Acts as the scheduling brain for one pet."""
    date: date
    pet: Pet
    available_time: int     # minutes budgeted for this pet today
    tasks: list[Task] = field(default_factory=list)

    def generate_plan(self) -> None:
        """Pull tasks from the pet, sort by priority, and fit within available_time."""
        priority_order = {"high": 0, "medium": 1, "low": 2}
        candidates = sorted(
            self.pet.get_tasks(),
            key=lambda t: priority_order.get(t.priority, 99),
        )

        self.tasks = []
        time_remaining = self.available_time
        for task in candidates:
            if not task.completed and task.duration <= time_remaining:
                self.tasks.append(task)
                time_remaining -= task.duration

    def display_plan(self) -> None:
        print(f"Schedule for {self.pet.name} on {self.date}")
        print(f"Available time: {self.available_time} min")
        print("-" * 32)
        if not self.tasks:
            print("  No tasks scheduled.")
        else:
            total = 0
            for task in self.tasks:
                status = "[x]" if task.completed else "[ ]"
                print(f"  {status} {task.name:<20} {task.duration:>3} min  [{task.priority}]")
                total += task.duration
            print("-" * 32)
            print(f"  Total: {total} min / {self.available_time} min available")


# ---------------------------------------------------------------------------
# Helper: build schedules for every pet an owner has
# ---------------------------------------------------------------------------
def build_owner_schedules(owner: Owner, schedule_date: date) -> list[Schedule]:
    """
    Traverse owner → pets → tasks to produce one Schedule per pet.

    Time is split evenly across pets; adjust the allocation logic as needed.
    """
    if not owner.pets:
        return []
    time_per_pet = owner.available_time // len(owner.pets)
    schedules = []
    for pet in owner.pets:
        s = Schedule(date=schedule_date, pet=pet, available_time=time_per_pet)
        s.generate_plan()
        schedules.append(s)
    return schedules
