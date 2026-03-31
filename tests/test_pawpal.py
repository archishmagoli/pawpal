from pawpal_system import Task, Pet


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
