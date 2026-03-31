from datetime import date
from pawpal_system import Task, Pet, Owner, build_owner_schedules, sort_tasks_by_time, filter_tasks, detect_conflicts

# --- Setup Owner ---
owner = Owner(name="Alex", available_time=120)  # 2 hours available today

# --- Create Pets ---
luna = Pet(name="Luna", age=3, species="Dog")
mochi = Pet(name="Mochi", age=5, species="Cat")

# --- Add Tasks OUT OF ORDER (priority mixed, not chronological) ---
luna.add_task(Task(name="Playtime",    duration=25, priority="low",    category="exercise"))
luna.add_task(Task(name="Morning Walk",duration=30, priority="high",   category="exercise"))
luna.add_task(Task(name="Grooming",    duration=20, priority="medium", category="hygiene"))
luna.add_task(Task(name="Breakfast",   duration=10, priority="high",   category="feeding",  completed=True))

mochi.add_task(Task(name="Vet Checkup",    duration=45, priority="medium", category="health"))
mochi.add_task(Task(name="Laser Playtime", duration=15, priority="low",    category="exercise"))
mochi.add_task(Task(name="Litter Box",     duration=5,  priority="high",   category="hygiene"))
mochi.add_task(Task(name="Breakfast",      duration=10, priority="high",   category="feeding"))

# --- Register Pets with Owner ---
owner.add_pet(luna)
owner.add_pet(mochi)

# --- Generate Schedules ---
today = date.today()
schedules = build_owner_schedules(owner, today)

# --- Today's Schedule (raw display) ---
print("=" * 40)
print(f"  TODAY'S SCHEDULE — {today}")
print(f"  Owner: {owner.name}  |  Total time: {owner.available_time} min")
print("=" * 40)
for schedule in schedules:
    schedule.display_plan()
    print()

# --- Sorted by start time ---
all_scheduled = [t for s in schedules for t in s.tasks]
print("=" * 40)
print("  SORTED BY START TIME (all pets)")
print("=" * 40)
for t in sort_tasks_by_time(all_scheduled):
    print(f"  {t.start_time}  {t.name:<20} [{t.priority}]")
print()

# --- Filter: pending tasks only ---
print("=" * 40)
print("  PENDING TASKS (all pets)")
print("=" * 40)
for t in filter_tasks(schedules, completed=False):
    print(f"  [ ] {t.name}")
print()

# --- Filter: completed tasks only ---
print("=" * 40)
print("  COMPLETED TASKS (all pets)")
print("=" * 40)
for t in filter_tasks(schedules, completed=True):
    print(f"  [x] {t.name}")
print()

# --- Filter: Luna's tasks only ---
print("=" * 40)
print("  LUNA'S TASKS ONLY")
print("=" * 40)
for t in filter_tasks(schedules, pet_name="Luna"):
    print(f"  {t.name:<20} completed={t.completed}")
print()

# --- Filter: Mochi's pending tasks ---
print("=" * 40)
print("  MOCHI — PENDING ONLY")
print("=" * 40)
for t in filter_tasks(schedules, pet_name="Mochi", completed=False):
    print(f"  [ ] {t.name}")
print()

# --- Recurring Tasks Demo ---
print("=" * 40)
print("  RECURRING TASKS DEMO")
print("=" * 40)

# Add recurring tasks to Luna
luna.add_task(Task(name="Daily Walk",    duration=20, priority="high",   category="exercise", recurrence="daily",  due_date=today))
luna.add_task(Task(name="Weekly Bath",   duration=30, priority="medium", category="hygiene",  recurrence="weekly", due_date=today))

def print_task_list(pet: Pet) -> None:
    print(f"  {pet.name}'s tasks ({len(pet.tasks)} total):")
    for t in pet.tasks:
        recur_label = f"  [{t.recurrence}]" if t.recurrence else ""
        due_label   = f"  due={t.due_date}" if t.due_date else ""
        status      = "[x]" if t.completed else "[ ]"
        print(f"    {status} {t.name:<22}{recur_label}{due_label}")

print("\nBEFORE completing recurring tasks:")
print_task_list(luna)

luna.complete_task("Daily Walk",  today)
luna.complete_task("Weekly Bath", today)

print("\nAFTER completing recurring tasks:")
print_task_list(luna)

# --- Conflict Detection Demo ---
print()
print("=" * 40)
print("  CONFLICT DETECTION DEMO")
print("=" * 40)

# Force a conflict: give Luna and Mochi overlapping start times manually
conflict_pet1 = Pet(name="Luna",  age=3, species="Dog")
conflict_pet2 = Pet(name="Mochi", age=5, species="Cat")

conflict_pet1.add_task(Task(name="Bath Time",   duration=20, priority="high", category="hygiene",  start_time="09:00"))
conflict_pet2.add_task(Task(name="Vet Checkup", duration=45, priority="high", category="health",   start_time="09:10"))  # overlaps Bath Time
conflict_pet1.add_task(Task(name="Lunch Feed",  duration=10, priority="high", category="feeding",  start_time="12:00"))
conflict_pet2.add_task(Task(name="Nap Check",   duration=15, priority="low",  category="exercise", start_time="14:00"))  # no conflict

from pawpal_system import Schedule
conflict_schedules = [
    Schedule(date=today, pet=conflict_pet1, available_time=60, tasks=conflict_pet1.get_tasks()),
    Schedule(date=today, pet=conflict_pet2, available_time=60, tasks=conflict_pet2.get_tasks()),
]

warnings = detect_conflicts(conflict_schedules)
if warnings:
    for w in warnings:
        print(f"  {w}")
else:
    print("  No conflicts detected.")
