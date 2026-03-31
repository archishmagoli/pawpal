from datetime import date, datetime, timedelta
from dataclasses import dataclass, field


@dataclass
class Task:
    name: str
    duration: int       # minutes
    priority: str       # "high", "medium", "low"
    category: str
    start_time: str | None = None
    completed: bool = False
    recurrence: str | None = None   # "daily" | "weekly" | None
    due_date: date | None = None    # date this task is due

    def mark_complete(self) -> "Task | None":
        """Mark this task as completed.

        For recurring tasks, returns a new Task instance for the next occurrence
        with completed=False and due_date advanced by the recurrence interval.
        Returns None if the task is not recurring.
        """
        self.completed = True
        if self.recurrence == "daily" and self.due_date is not None:
            return Task(
                name=self.name,
                duration=self.duration,
                priority=self.priority,
                category=self.category,
                recurrence=self.recurrence,
                due_date=self.due_date + timedelta(days=1),
            )
        if self.recurrence == "weekly" and self.due_date is not None:
            return Task(
                name=self.name,
                duration=self.duration,
                priority=self.priority,
                category=self.category,
                recurrence=self.recurrence,
                due_date=self.due_date + timedelta(weeks=1),
            )
        return None


@dataclass
class Pet:
    name: str
    age: int
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Append a task to this pet's task list."""
        self.tasks.append(task)

    def remove_task(self, name: str) -> None:
        """Remove a task by name from this pet's task list."""
        self.tasks = [t for t in self.tasks if t.name != name]

    def get_tasks(self) -> list[Task]:
        """Return a copy of this pet's task list."""
        return list(self.tasks)

    def complete_task(self, name: str, on_date: date) -> None:
        """Mark a task as complete by name and handle recurring scheduling.

        Finds the task matching `name`, calls mark_complete() on it, and if a
        next-occurrence Task is returned (for recurring tasks), appends it to
        self.tasks. The `on_date` parameter represents the date being completed;
        the new occurrence's due_date is set automatically by mark_complete().
        """
        for task in self.tasks:
            if task.name == name:
                if task.due_date is None:
                    task.due_date = on_date
                next_task = task.mark_complete()
                if next_task is not None:
                    self.tasks.append(next_task)
                return


@dataclass
class Owner:
    name: str
    available_time: int     # total minutes available per day
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's pet list."""
        self.pets.append(pet)

    def remove_pet(self, name: str) -> None:
        """Remove a pet by name from this owner's pet list."""
        self.pets = [p for p in self.pets if p.name != name]

    def get_pet(self, name: str) -> Pet | None:
        """Return the first pet matching the given name, or None."""
        return next((p for p in self.pets if p.name == name), None)


@dataclass
class Schedule:
    """Per-pet daily schedule. Acts as the scheduling brain for one pet."""
    date: date
    pet: Pet
    available_time: int     # minutes budgeted for this pet today
    tasks: list[Task] = field(default_factory=list)

    def generate_plan(self) -> None:
        """Pull tasks from the pet, sort by priority, fit within available_time, then assign start times."""
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

        # Assign sequential start times beginning at 08:00
        current = datetime(self.date.year, self.date.month, self.date.day, 8, 0)
        for task in self.tasks:
            task.start_time = current.strftime("%H:%M")
            current += timedelta(minutes=task.duration)

    def display_plan(self) -> None:
        """Print the scheduled tasks for this pet to stdout."""
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
# Helpers
# ---------------------------------------------------------------------------
def sort_tasks_by_time(tasks: list[Task]) -> list[Task]:
    """Return tasks sorted chronologically by start_time; unscheduled tasks go last.

    "HH:MM" strings are zero-padded, so lexicographic order equals chronological
    order — no datetime parsing required. Tasks with no start_time assigned are
    pushed to the end via the "99:99" sentinel fallback.

    Args:
        tasks: Flat list of Task objects to sort. May include unscheduled tasks.

    Returns:
        A new sorted list; the original list is not modified.

    Usage:
        sort_tasks_by_time(schedule.tasks)                           # one pet
        sort_tasks_by_time([t for s in schedules for t in s.tasks]) # all pets
    """
    return sorted(tasks, key=lambda t: t.start_time or "99:99")


def filter_tasks(
    schedules: list["Schedule"],
    *,
    completed: bool | None = None,
    pet_name: str | None = None,
) -> list[Task]:
    """Filter tasks across schedules by pet name and/or completion status.

    Both filters are keyword-only to prevent accidental positional misuse.
    Omit either filter to match all values for that dimension. Draws from each
    pet's full raw task list (pet.get_tasks()), so completed tasks are visible
    even though generate_plan() excludes them from the scheduled plan.

    Args:
        schedules:  List of Schedule objects covering one or more pets.
        completed:  True → completed tasks only; False → pending only; None → all.
        pet_name:   Exact pet name to isolate; None matches every pet.

    Returns:
        Flat list of Task objects matching all supplied filters.

    Usage:
        filter_tasks(schedules)                                    # all tasks
        filter_tasks(schedules, completed=False)                   # pending only
        filter_tasks(schedules, completed=True)                    # completed only
        filter_tasks(schedules, pet_name="Luna")                   # one pet, any status
        filter_tasks(schedules, pet_name="Luna", completed=False)  # combine both
    """
    result = []
    for s in schedules:
        if pet_name is not None and s.pet.name != pet_name:
            continue
        for t in s.pet.get_tasks():
            if completed is None or t.completed == completed:
                result.append(t)
    return result



def detect_conflicts(schedules: list[Schedule]) -> list[str]:
    """Return warning strings for any tasks whose time windows overlap across all schedules.

    Uses lightweight integer-minute arithmetic — no datetime parsing, no exceptions raised.
    Two tasks conflict when their intervals overlap: a_start < b_end and b_start < a_end.
    Skips any task that has not yet been assigned a start_time. Checks all pairs,
    including tasks belonging to different pets (cross-pet conflicts).

    Args:
        schedules: List of Schedule objects, each containing a pet and its tasks.

    Returns:
        List of human-readable warning strings, one per conflicting pair.
        Empty list if no conflicts are found.

    Usage:
        warnings = detect_conflicts(schedules)
        for w in warnings:
            print(w)
    """
    # Flatten to (pet_name, task) pairs — skip tasks with no start time assigned
    entries = [
        (s.pet.name, t)
        for s in schedules
        for t in s.tasks
        if t.start_time is not None
    ]

    def to_minutes(hhmm: str) -> int:
        h, m = hhmm.split(":")
        return int(h) * 60 + int(m)

    warnings = []
    for i, (pet_a, task_a) in enumerate(entries):
        a_start = to_minutes(task_a.start_time)
        a_end   = a_start + task_a.duration
        for pet_b, task_b in entries[i + 1:]:
            b_start = to_minutes(task_b.start_time)
            b_end   = b_start + task_b.duration
            if a_start < b_end and b_start < a_end:
                warnings.append(
                    f"WARNING: '{task_a.name}' ({pet_a}, {task_a.start_time}–{a_end // 60:02d}:{a_end % 60:02d}) "
                    f"conflicts with '{task_b.name}' ({pet_b}, {task_b.start_time}–{b_end // 60:02d}:{b_end % 60:02d})"
                )
    return warnings


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
