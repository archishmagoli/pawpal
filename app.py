import streamlit as st
from datetime import date
from pawpal_system import Owner, Pet, Task, Schedule

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

# ---------------------------------------------------------------------------
# Session state initialization
# ---------------------------------------------------------------------------
# Streamlit reruns this entire script on every widget interaction.
# The "not in" guard ensures each object is created only ONCE per session,
# even though the code at the top of the file runs on every rerender.
# Think of st.session_state as a dictionary that survives reruns.
# ---------------------------------------------------------------------------
if "owner" not in st.session_state:
    st.session_state.owner = None
if "pet" not in st.session_state:
    st.session_state.pet = None
if "schedule" not in st.session_state:
    st.session_state.schedule = None

# ---------------------------------------------------------------------------
# Section 1: Owner & Pet Setup
# ---------------------------------------------------------------------------
st.subheader("Owner & Pet Setup")

owner_name = st.text_input("Owner name", value="Jordan")
available_time = st.number_input(
    "Your available time today (minutes)", min_value=10, max_value=480, value=60
)
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
pet_age = st.number_input("Pet age (years)", min_value=0, max_value=30, value=3)

if st.button("Save Owner & Pet"):
    # Build real objects from our pawpal_system module
    pet = Pet(name=pet_name, age=int(pet_age), species=species)
    owner = Owner(name=owner_name, available_time=int(available_time))
    owner.add_pet(pet)

    # Store in the session vault — these persist across all reruns
    st.session_state.owner = owner
    st.session_state.pet = pet
    st.session_state.schedule = None   # reset any old schedule
    st.success(f"Saved! Owner: {owner_name} | Pet: {pet_name} ({species}, age {pet_age})")

# Don't render the rest of the app until setup is complete
if st.session_state.owner is None:
    st.info("Fill in the form above and click **Save Owner & Pet** to get started.")
    st.stop()

st.divider()

# ---------------------------------------------------------------------------
# Section 2: Task Entry
# ---------------------------------------------------------------------------
st.subheader(f"Tasks for {st.session_state.pet.name}")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
    category = st.text_input("Category", value="exercise")

if st.button("Add task"):
    task = Task(
        name=task_title,
        duration=int(duration),
        priority=priority,
        category=category,
    )
    st.session_state.pet.add_task(task)
    st.success(f"Added: {task_title} ({duration} min, {priority})")

# Display current tasks straight from the Pet object
pet_tasks = st.session_state.pet.get_tasks()
if pet_tasks:
    st.table(
        [
            {
                "Task": t.name,
                "Duration (min)": t.duration,
                "Priority": t.priority,
                "Category": t.category,
                "Done": "Yes" if t.completed else "No",
            }
            for t in pet_tasks
        ]
    )
else:
    st.info("No tasks yet. Add one above.")

st.divider()

# ---------------------------------------------------------------------------
# Section 3: Schedule Generation
# ---------------------------------------------------------------------------
st.subheader("Build Schedule")
st.caption(
    f"Scheduler will pick tasks for {st.session_state.pet.name} "
    f"that fit within {st.session_state.owner.available_time} minutes, "
    "sorted by priority."
)

if st.button("Generate schedule"):
    owner = st.session_state.owner
    pet = st.session_state.pet
    # Schedule is the "brain": it retrieves tasks from the pet and builds a plan
    schedule = Schedule(
        date=date.today(),
        pet=pet,
        available_time=owner.available_time,
    )
    schedule.generate_plan()
    st.session_state.schedule = schedule  # save result to session vault

if st.session_state.schedule:
    schedule = st.session_state.schedule
    st.success(f"Schedule for **{schedule.pet.name}** on {schedule.date}")

    if schedule.tasks:
        st.table(
            [
                {
                    "Task": t.name,
                    "Duration (min)": t.duration,
                    "Priority": t.priority,
                    "Category": t.category,
                }
                for t in schedule.tasks
            ]
        )
        total = sum(t.duration for t in schedule.tasks)
        remaining = schedule.available_time - total
        col_a, col_b = st.columns(2)
        col_a.metric("Time scheduled", f"{total} min")
        col_b.metric("Time remaining", f"{remaining} min")
    else:
        st.warning(
            "No tasks fit within the available time, or all tasks are already completed."
        )
