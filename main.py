from datetime import date
from pawpal_system import Task, Pet, Owner, Schedule
from pawpal_system import build_owner_schedules, sort_tasks_by_time, filter_tasks, detect_conflicts

PRIORITY_EMOJI = {"high": "🔴", "medium": "🟡", "low": "🟢"}

# --- Setup ---
owner = Owner(name="Alex", available_time=120)
luna  = Pet(name="Luna",  age=3, species="Dog")
mochi = Pet(name="Mochi", age=5, species="Cat")
today = date.today()

luna.add_task(Task(name="Morning Walk", duration=30, priority="high",   category="exercise"))
luna.add_task(Task(name="Grooming",     duration=20, priority="medium", category="hygiene"))
luna.add_task(Task(name="Playtime",     duration=25, priority="low",    category="exercise"))
luna.add_task(Task(name="Daily Walk",   duration=20, priority="high",   category="exercise", recurrence="daily", due_date=today))

mochi.add_task(Task(name="Litter Box",     duration=5,  priority="high",   category="hygiene"))
mochi.add_task(Task(name="Vet Checkup",    duration=45, priority="medium", category="health"))
mochi.add_task(Task(name="Laser Playtime", duration=15, priority="low",    category="exercise"))

owner.add_pet(luna)
owner.add_pet(mochi)

# --- Generate & display schedules ---
schedules = build_owner_schedules(owner, today)
print(f"\n{'='*40}\n  TODAY'S SCHEDULE — {today}\n{'='*40}")
for s in schedules:
    s.display_plan()

# --- Sorted by start time with priority emoji ---
print(f"\n{'='*40}\n  SORTED BY TIME (all pets)\n{'='*40}")
for t in sort_tasks_by_time([t for s in schedules for t in s.tasks]):
    print(f"  {t.start_time}  {PRIORITY_EMOJI[t.priority]} {t.name}")

# --- Pending tasks ---
print(f"\n{'='*40}\n  PENDING TASKS\n{'='*40}")
for t in filter_tasks(schedules, completed=False):
    print(f"  [ ] {PRIORITY_EMOJI[t.priority]} {t.name}")

# --- Recurring task demo ---
print(f"\n{'='*40}\n  RECURRING TASKS DEMO\n{'='*40}")
print(f"  Luna has {len(luna.tasks)} tasks before completing Daily Walk")
luna.complete_task("Daily Walk", today)
print(f"  Luna has {len(luna.tasks)} tasks after — next due: {luna.tasks[-1].due_date}")

# --- Conflict detection ---
print(f"\n{'='*40}\n  CONFLICT DETECTION\n{'='*40}")
c1 = Pet(name="Luna",  age=3, species="Dog")
c2 = Pet(name="Mochi", age=5, species="Cat")
c1.add_task(Task(name="Bath Time",   duration=20, priority="high", category="hygiene", start_time="09:00"))
c2.add_task(Task(name="Vet Checkup", duration=45, priority="high", category="health",  start_time="09:10"))
conflict_schedules = [
    Schedule(date=today, pet=c1, available_time=60, tasks=c1.get_tasks()),
    Schedule(date=today, pet=c2, available_time=60, tasks=c2.get_tasks()),
]
for w in detect_conflicts(conflict_schedules):
    print(f"  {w}")
