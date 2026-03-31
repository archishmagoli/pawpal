from datetime import date
from pawpal_system import Task, Pet, Owner, build_owner_schedules

# --- Setup Owner ---
owner = Owner(name="Alex", available_time=120)  # 2 hours available today

# --- Create Pets ---
luna = Pet(name="Luna", age=3, species="Dog")
mochi = Pet(name="Mochi", age=5, species="Cat")

# --- Add Tasks to Luna (Dog) ---
luna.add_task(Task(name="Morning Walk",    duration=30, priority="high",   category="exercise"))
luna.add_task(Task(name="Breakfast",       duration=10, priority="high",   category="feeding"))
luna.add_task(Task(name="Grooming",        duration=20, priority="medium", category="hygiene"))
luna.add_task(Task(name="Playtime",        duration=25, priority="low",    category="exercise"))

# --- Add Tasks to Mochi (Cat) ---
mochi.add_task(Task(name="Breakfast",      duration=10, priority="high",   category="feeding"))
mochi.add_task(Task(name="Litter Box",     duration=5,  priority="high",   category="hygiene"))
mochi.add_task(Task(name="Vet Checkup",    duration=45, priority="medium", category="health"))
mochi.add_task(Task(name="Laser Playtime", duration=15, priority="low",    category="exercise"))

# --- Register Pets with Owner ---
owner.add_pet(luna)
owner.add_pet(mochi)

# --- Generate Schedules ---
today = date.today()
schedules = build_owner_schedules(owner, today)

# --- Print Today's Schedule ---
print("=" * 40)
print(f"  TODAY'S SCHEDULE — {today}")
print(f"  Owner: {owner.name}  |  Total time: {owner.available_time} min")
print("=" * 40)

for schedule in schedules:
    schedule.display_plan()
    print()
