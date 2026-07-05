"""Terminal testing ground for pawpal_system.py."""

from datetime import date

from pawpal_system import Owner, Pet, Task


def main():
    owner = Owner("Jordan", 29, date(1996, 4, 12), minutes_available=60)

    dog = Pet("Biscuit", "dog", "Golden Retriever", 4)
    cat = Pet("Mochi", "cat", "Tabby", 2)
    owner.add_pet(dog)
    owner.add_pet(cat)

    dog.add_task(Task("Morning walk", 30, "high"))
    dog.add_task(Task("Grooming", 45, "low"))
    cat.add_task(Task("Feeding", 10, "high"))
    cat.add_task(Task("Litter box cleaning", 15, "medium"))

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


if __name__ == "__main__":
    main()
