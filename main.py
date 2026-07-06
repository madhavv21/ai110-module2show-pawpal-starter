"""Terminal testing ground for pawpal_system.py."""

from datetime import date, time

from pawpal_system import Owner, Pet, Task


def main():
    owner = Owner("Jordan", 29, date(1996, 4, 12), minutes_available=60)

    dog = Pet("Biscuit", "dog", "Golden Retriever", 4)
    cat = Pet("Mochi", "cat", "Tabby", 2)
    owner.add_pet(dog)
    owner.add_pet(cat)

    # Tasks are added out of chronological order on purpose, to exercise sort_by_time().
    grooming = Task("Grooming", 45, "low", scheduled_time=time(17, 0))
    litter = Task("Litter box cleaning", 15, "medium", scheduled_time=time(12, 30))
    walk = Task("Morning walk", 30, "high", scheduled_time=time(8, 0))
    feeding = Task("Feeding", 10, "high", scheduled_time=time(7, 30), recurring="daily")
    no_time_task = Task("Vet follow-up call", 5, "medium")
    # Scheduled at the same date/time as `walk`, on purpose, to exercise find_time_conflicts().
    training = Task("Training session", 10, "medium", scheduled_time=time(8, 0), scheduled_date=walk.get_scheduled_date())

    dog.add_task(grooming)
    dog.add_task(walk)
    dog.add_task(no_time_task)
    dog.add_task(training)
    cat.add_task(feeding)
    cat.add_task(litter)

    # Feeding is a daily recurring task: completing it should auto-schedule tomorrow's feeding.
    cat.complete_task(feeding.task_id)

    print("Recurring task auto-renewal")
    print("=" * 40)
    print(f"Completed: {feeding.get_title()} on {feeding.get_scheduled_date()} (done={feeding.is_done()})")
    next_feeding = next(
        t for t in cat.get_tasks() if t.get_title() == feeding.get_title() and t.task_id != feeding.task_id
    )
    print(
        f"Next occurrence auto-created: {next_feeding.get_title()} on "
        f"{next_feeding.get_scheduled_date()} (done={next_feeding.is_done()})"
    )
    print()

    plan = owner.generate_plan()
    pets_by_id = {pet.pet_id: pet for pet in owner.get_pets()}

    print("Today's Schedule")
    print("=" * 40)
    for task in plan:
        pet = pets_by_id[task.pet_id]
        print(f"{pet.get_name()}: {task.get_title()} ({task.get_duration()} min) [priority: {task.get_priority()}]")

    print()
    print("Why this plan:")
    print(owner.explain_plan())

    print()
    print("All tasks sorted by scheduled time")
    print("=" * 40)
    all_tasks = owner.filter_tasks()
    for task in owner.scheduler.sort_by_time(all_tasks):
        pet = pets_by_id[task.pet_id]
        scheduled = task.get_scheduled_time()
        time_label = scheduled.strftime("%H:%M") if scheduled else "unscheduled"
        print(f"{time_label} — {pet.get_name()}: {task.get_title()}")

    print()
    print("Tasks filtered by completion status")
    print("=" * 40)
    print("Not done:", [task.get_title() for task in owner.filter_tasks(done=False)])
    print("Done:", [task.get_title() for task in owner.filter_tasks(done=True)])

    print()
    print("Tasks filtered by pet name ('biscuit')")
    print("=" * 40)
    print([task.get_title() for task in owner.filter_tasks(pet_name="biscuit")])

    print()
    print("Scheduling conflicts (same date and time)")
    print("=" * 40)
    conflict_warnings = owner.explain_conflicts()
    if not conflict_warnings:
        print("No conflicts found.")
    else:
        for warning in conflict_warnings:
            print(warning)


if __name__ == "__main__":
    main()
