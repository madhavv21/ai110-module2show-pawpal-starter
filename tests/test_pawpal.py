from pawpal_system import Pet, Task


def test_mark_done_changes_task_status():
    task = Task("Morning walk", 30, "high")
    assert task.is_done() is False

    task.mark_done()

    assert task.is_done() is True


def test_add_task_increases_pet_task_count():
    pet = Pet("Biscuit", "dog", "Golden Retriever", 4)
    assert len(pet.get_tasks()) == 0

    pet.add_task(Task("Feeding", 10, "high"))

    assert len(pet.get_tasks()) == 1
