from datetime import date

from pawpal_system import Task, Pet, Schedule, detect_conflicts, sort_tasks_by_time


def test_mark_complete_changes_status():
    task = Task(name="Walk", duration=30, priority="high", category="exercise")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Luna", age=3, species="Dog")
    assert len(pet.get_tasks()) == 0
    pet.add_task(Task(name="Breakfast", duration=10, priority="high", category="feeding"))
    pet.add_task(Task(name="Walk", duration=30, priority="medium", category="exercise"))
    assert len(pet.get_tasks()) == 2


def test_sort_tasks_by_time_returns_chronological_order():
    t1 = Task(name="Dinner",    duration=15, priority="high",   category="feeding",  start_time="18:00")
    t2 = Task(name="Morning",   duration=10, priority="high",   category="feeding",  start_time="08:00")
    t3 = Task(name="Afternoon", duration=30, priority="medium", category="exercise", start_time="13:30")

    sorted_tasks = sort_tasks_by_time([t1, t2, t3])

    assert [t.start_time for t in sorted_tasks] == ["08:00", "13:30", "18:00"]


def test_sort_tasks_unscheduled_tasks_go_last():
    t_scheduled   = Task(name="Walk",  duration=30, priority="high", category="exercise", start_time="09:00")
    t_unscheduled = Task(name="Groom", duration=20, priority="low",  category="grooming", start_time=None)

    sorted_tasks = sort_tasks_by_time([t_unscheduled, t_scheduled])

    assert sorted_tasks[0].name == "Walk"
    assert sorted_tasks[1].name == "Groom"


def test_daily_recurrence_creates_next_day_task():
    today = date(2026, 3, 30)
    task = Task(name="Feed", duration=10, priority="high", category="feeding",
                recurrence="daily", due_date=today)

    next_task = task.mark_complete()

    assert task.completed is True
    assert next_task is not None
    assert next_task.due_date == date(2026, 3, 31)
    assert next_task.completed is False
    assert next_task.recurrence == "daily"


def test_daily_recurrence_via_pet_appends_new_task():
    today = date(2026, 3, 30)
    pet = Pet(name="Luna", age=3, species="Dog")
    pet.add_task(Task(name="Feed", duration=10, priority="high", category="feeding",
                      recurrence="daily", due_date=today))

    pet.complete_task("Feed", on_date=today)

    tasks = pet.get_tasks()
    assert len(tasks) == 2
    new_task = next(t for t in tasks if not t.completed)
    assert new_task.due_date == date(2026, 3, 31)


def test_detect_conflicts_flags_overlapping_tasks():
    pet = Pet(name="Luna", age=3, species="Dog")
    t1 = Task(name="Walk",  duration=60, priority="high",   category="exercise", start_time="08:00")
    t2 = Task(name="Feed",  duration=15, priority="high",   category="feeding",  start_time="08:30")  # overlaps t1

    schedule = Schedule(date=date(2026, 3, 30), pet=pet, available_time=120, tasks=[t1, t2])
    warnings = detect_conflicts([schedule])

    assert len(warnings) == 1
    assert "Walk" in warnings[0]
    assert "Feed" in warnings[0]


def test_detect_conflicts_no_false_positives():
    pet = Pet(name="Luna", age=3, species="Dog")
    t1 = Task(name="Walk",  duration=30, priority="high", category="exercise", start_time="08:00")
    t2 = Task(name="Feed",  duration=15, priority="high", category="feeding",  start_time="08:30")  # starts exactly when t1 ends

    schedule = Schedule(date=date(2026, 3, 30), pet=pet, available_time=120, tasks=[t1, t2])
    warnings = detect_conflicts([schedule])

    assert warnings == []
