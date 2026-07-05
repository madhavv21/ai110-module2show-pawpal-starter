"""PawPal+ core classes, implemented from diagrams/uml.mmd."""

import uuid
from datetime import date

PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


class Task:
    def __init__(self, title: str, duration_minutes: int, priority: str, category: str = "general", recurring: bool = False):
        """Create a new task with a freshly generated task_id and done=False."""
        self.task_id = str(uuid.uuid4())
        self.pet_id = None  # set by Pet.add_task() once the task is attached to a pet
        self.title = title
        self.duration_minutes = duration_minutes
        self.priority = priority
        self.category = category
        self.recurring = recurring
        self.done = False

    def get_title(self) -> str:
        """Return the task's title."""
        return self.title

    def set_title(self, title: str) -> None:
        """Update the task's title."""
        self.title = title

    def get_duration(self) -> int:
        """Return the task's duration in minutes."""
        return self.duration_minutes

    def set_duration(self, minutes: int) -> None:
        """Update the task's duration in minutes."""
        self.duration_minutes = minutes

    def get_priority(self) -> str:
        """Return the task's priority ('low', 'medium', or 'high')."""
        return self.priority

    def set_priority(self, priority: str) -> None:
        """Update the task's priority."""
        self.priority = priority

    def get_category(self) -> str:
        """Return the task's category."""
        return self.category

    def set_category(self, category: str) -> None:
        """Update the task's category."""
        self.category = category

    def is_recurring(self) -> bool:
        """Return whether the task repeats (e.g. daily) rather than being one-off."""
        return self.recurring

    def set_recurring(self, recurring: bool) -> None:
        """Update whether the task repeats."""
        self.recurring = recurring

    def is_done(self) -> bool:
        """Return whether the task has been completed."""
        return self.done

    def mark_done(self) -> None:
        """Mark the task as completed."""
        self.done = True


class Pet:
    def __init__(self, name: str, species: str, breed: str, age: int):
        """Create a new pet with a freshly generated pet_id and an empty task list."""
        self.pet_id = str(uuid.uuid4())
        self.name = name
        self.species = species
        self.breed = breed
        self.age = age
        self.tasks = []

    def get_name(self) -> str:
        """Return the pet's name."""
        return self.name

    def set_name(self, name: str) -> None:
        """Update the pet's name."""
        self.name = name

    def get_species(self) -> str:
        """Return the pet's species."""
        return self.species

    def describe(self) -> str:
        """Return a short human-readable summary of the pet."""
        return f"{self.name} is a {self.age}-year-old {self.breed} {self.species}."

    def add_task(self, task: Task) -> None:
        """Attach a task to this pet, stamping the task with this pet's id."""
        task.pet_id = self.pet_id
        self.tasks.append(task)

    def edit_task(self, task_id: str, changes: dict) -> None:
        """Apply a dict of field changes to one of this pet's tasks via its setters."""
        task = self._find_task(task_id)
        if task is None:
            raise ValueError(f"No task with id {task_id} for pet {self.name}")
        setters = {
            "title": task.set_title,
            "duration_minutes": task.set_duration,
            "priority": task.set_priority,
            "category": task.set_category,
            "recurring": task.set_recurring,
        }
        for field, value in changes.items():
            if field not in setters:
                raise ValueError(f"Unknown task field: {field}")
            setters[field](value)

    def remove_task(self, task_id: str) -> None:
        """Remove one of this pet's tasks by id."""
        self.tasks = [task for task in self.tasks if task.task_id != task_id]

    def get_tasks(self) -> list:
        """Return a copy of this pet's task list."""
        return list(self.tasks)

    def _find_task(self, task_id: str):
        """Return the task with the given id, or None if not found."""
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        return None


class Scheduler:
    def __init__(self):
        """Create a scheduler with no plan generated yet."""
        self.planned = []
        self.skipped = []

    def get_all_tasks(self, pets: list) -> list:
        """Return every task across all given pets, flattened into one list."""
        all_tasks = []
        for pet in pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks

    def sort_by_priority(self, tasks: list) -> list:
        """Return tasks ordered high-to-low priority, shorter tasks first within a tier."""
        return sorted(
            tasks,
            key=lambda task: (PRIORITY_ORDER.get(task.get_priority(), len(PRIORITY_ORDER)), task.get_duration()),
        )

    def generate_plan(self, pets: list, minutes_available: int) -> list:
        """Build today's plan by greedily fitting the highest-priority tasks into the time budget."""
        self.planned = []
        self.skipped = []

        active_tasks = [task for task in self.get_all_tasks(pets) if not task.is_done()]
        ordered_tasks = self.sort_by_priority(active_tasks)

        remaining_minutes = minutes_available
        for task in ordered_tasks:
            if task.get_duration() <= remaining_minutes:
                self.planned.append(task)
                remaining_minutes -= task.get_duration()
            else:
                self.skipped.append(task)

        return self.planned

    def explain_plan(self) -> str:
        """Return a human-readable explanation of which tasks were scheduled or skipped, and why."""
        if not self.planned and not self.skipped:
            return "No plan has been generated yet."

        lines = []
        for task in self.planned:
            lines.append(f"- {task.get_title()} ({task.get_duration()} min, {task.get_priority()} priority): scheduled.")
        for task in self.skipped:
            lines.append(
                f"- {task.get_title()} ({task.get_duration()} min, {task.get_priority()} priority): "
                "skipped, not enough time remaining."
            )
        return "\n".join(lines)


class Owner:
    def __init__(self, name: str, age: int, dob: date, minutes_available: int):
        """Create a new owner with no pets yet and a dedicated Scheduler."""
        self.name = name
        self.age = age
        self.dob = dob
        self.minutes_available = minutes_available
        self.pets = []
        self.scheduler = Scheduler()

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's list of pets."""
        self.pets.append(pet)

    def remove_pet(self, pet_id: str) -> None:
        """Remove one of this owner's pets by id."""
        self.pets = [pet for pet in self.pets if pet.pet_id != pet_id]

    def get_pets(self) -> list:
        """Return a copy of this owner's pet list."""
        return list(self.pets)

    def get_minutes_available(self) -> int:
        """Return how many minutes this owner has available today."""
        return self.minutes_available

    def set_minutes_available(self, minutes: int) -> None:
        """Update how many minutes this owner has available today."""
        self.minutes_available = minutes

    def generate_plan(self) -> list:
        """Generate today's plan across all of this owner's pets."""
        return self.scheduler.generate_plan(self.pets, self.minutes_available)

    def explain_plan(self) -> str:
        """Explain the most recently generated plan."""
        return self.scheduler.explain_plan()
