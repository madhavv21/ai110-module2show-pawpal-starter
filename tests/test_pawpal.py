from datetime import date, time

from pawpal_system import Owner, Pet, Scheduler, Task


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


def test_completing_recurring_task_schedules_next_occurrence():
    pet = Pet("Mochi", "cat", "Tabby", 2)
    task = Task("Feeding", 10, "high", recurring="daily", scheduled_date=date(2026, 7, 6))
    pet.add_task(task)

    pet.complete_task(task.task_id)

    assert task.is_done() is True
    assert len(pet.get_tasks()) == 2
    next_task = next(t for t in pet.get_tasks() if t.task_id != task.task_id)
    assert next_task.get_title() == "Feeding"
    assert next_task.is_done() is False
    assert next_task.get_scheduled_date() == date(2026, 7, 7)
    assert next_task.get_recurrence_frequency() == "daily"


def test_completing_non_recurring_task_does_not_create_new_task():
    pet = Pet("Biscuit", "dog", "Golden Retriever", 4)
    task = Task("Vet visit", 30, "high")
    pet.add_task(task)

    pet.complete_task(task.task_id)

    assert task.is_done() is True
    assert len(pet.get_tasks()) == 1


def test_weekly_and_monthly_recurrence_advance_correctly():
    weekly = Task("Grooming", 45, "low", recurring="weekly", scheduled_date=date(2026, 7, 6))
    assert weekly.next_occurrence().get_scheduled_date() == date(2026, 7, 13)

    monthly = Task("Vet checkup", 30, "medium", recurring="monthly", scheduled_date=date(2026, 1, 31))
    assert monthly.next_occurrence().get_scheduled_date() == date(2026, 2, 28)


def test_find_time_conflicts_detects_same_slot_across_pets():
    owner = Owner("Jordan", 29, date(1996, 4, 12), minutes_available=60)
    dog = Pet("Biscuit", "dog", "Golden Retriever", 4)
    cat = Pet("Mochi", "cat", "Tabby", 2)
    owner.add_pet(dog)
    owner.add_pet(cat)

    walk = Task("Morning walk", 30, "high", scheduled_time=time(8, 0), scheduled_date=date(2026, 7, 6))
    feeding = Task("Feeding", 10, "high", scheduled_time=time(8, 0), scheduled_date=date(2026, 7, 6))
    grooming = Task("Grooming", 45, "low", scheduled_time=time(17, 0), scheduled_date=date(2026, 7, 6))
    dog.add_task(walk)
    dog.add_task(grooming)
    cat.add_task(feeding)

    conflicts = owner.find_time_conflicts()

    assert len(conflicts) == 1
    conflicting_ids = {task.task_id for task in conflicts[0]}
    assert conflicting_ids == {walk.task_id, feeding.task_id}


def test_find_time_conflicts_ignores_unscheduled_and_different_dates():
    scheduler = Scheduler()
    pet = Pet("Biscuit", "dog", "Golden Retriever", 4)
    same_time_different_day = Task(
        "Walk", 30, "high", scheduled_time=time(8, 0), scheduled_date=date(2026, 7, 7)
    )
    pet.add_task(Task("Walk", 30, "high", scheduled_time=time(8, 0), scheduled_date=date(2026, 7, 6)))
    pet.add_task(same_time_different_day)
    pet.add_task(Task("Unscheduled task", 10, "low"))

    conflicts = scheduler.find_time_conflicts([pet])

    assert conflicts == []


def test_explain_conflicts_returns_warning_messages_without_raising():
    owner = Owner("Jordan", 29, date(1996, 4, 12), minutes_available=60)
    dog = Pet("Biscuit", "dog", "Golden Retriever", 4)
    owner.add_pet(dog)
    dog.add_task(Task("Morning walk", 30, "high", scheduled_time=time(8, 0), scheduled_date=date(2026, 7, 6)))
    dog.add_task(Task("Training session", 10, "medium", scheduled_time=time(8, 0), scheduled_date=date(2026, 7, 6)))

    warnings = owner.explain_conflicts()

    assert len(warnings) == 1
    assert "Morning walk" in warnings[0]
    assert "Training session" in warnings[0]
    assert warnings[0].startswith("Warning:")


def test_explain_conflicts_returns_empty_list_when_no_conflicts():
    owner = Owner("Jordan", 29, date(1996, 4, 12), minutes_available=60)
    dog = Pet("Biscuit", "dog", "Golden Retriever", 4)
    owner.add_pet(dog)
    dog.add_task(Task("Morning walk", 30, "high", scheduled_time=time(8, 0)))

    assert owner.explain_conflicts() == []
