"""PawPal+ core classes, implemented from diagrams/uml.mmd."""

import uuid
from datetime import date, time, timedelta

PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}

# Valid Task.recurring values. None (or "none") means the task is one-off.
RECURRENCE_FREQUENCIES = ("daily", "weekly", "monthly")


def _advance_date(base_date: date, frequency: str) -> date:
    """Return the next occurrence of base_date for the given recurrence frequency."""
    if frequency == "daily":
        return base_date + timedelta(days=1)
    if frequency == "weekly":
        return base_date + timedelta(weeks=1)
    if frequency == "monthly":
        month = base_date.month + 1
        year = base_date.year + (month - 1) // 12
        month = (month - 1) % 12 + 1
        day = min(base_date.day, _days_in_month(year, month))
        return date(year, month, day)
    raise ValueError(f"Unknown recurrence frequency: {frequency}")


def _days_in_month(year: int, month: int) -> int:
    """Return how many days are in the given year/month."""
    if month == 12:
        next_month_first = date(year + 1, 1, 1)
    else:
        next_month_first = date(year, month + 1, 1)
    return (next_month_first - timedelta(days=1)).day


class Task:
    def __init__(
        self,
        title: str,
        duration_minutes: int,
        priority: str,
        category: str = "general",
        recurring: str = None,
        scheduled_time: time = None,
        scheduled_date: date = None,
    ):
        """Create a new task with a freshly generated task_id and done=False.

        recurring is one of None (one-off), "daily", "weekly", or "monthly".
        scheduled_date defaults to today and is used to compute the next occurrence
        when a recurring task is completed.
        """
        if recurring is not None and recurring not in RECURRENCE_FREQUENCIES:
            raise ValueError(f"Unknown recurrence frequency: {recurring}")
        self.task_id = str(uuid.uuid4())
        self.pet_id = None  # set by Pet.add_task() once the task is attached to a pet
        self.title = title
        self.duration_minutes = duration_minutes
        self.priority = priority
        self.category = category
        self.recurring = recurring
        self.scheduled_time = scheduled_time
        self.scheduled_date = scheduled_date if scheduled_date is not None else date.today()
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
        """Return whether the task repeats (has a recurrence frequency) rather than being one-off."""
        return self.recurring is not None

    def get_recurrence_frequency(self):
        """Return the task's recurrence frequency ("daily", "weekly", "monthly", or None)."""
        return self.recurring

    def set_recurring(self, recurring: str) -> None:
        """Update the task's recurrence frequency (None, "daily", "weekly", or "monthly")."""
        if recurring is not None and recurring not in RECURRENCE_FREQUENCIES:
            raise ValueError(f"Unknown recurrence frequency: {recurring}")
        self.recurring = recurring

    def get_scheduled_time(self):
        """Return the task's preferred time of day (a datetime.time), or None if unset."""
        return self.scheduled_time

    def set_scheduled_time(self, scheduled_time) -> None:
        """Update the task's preferred time of day."""
        self.scheduled_time = scheduled_time

    def get_scheduled_date(self) -> date:
        """Return the date this task occurrence is scheduled for."""
        return self.scheduled_date

    def set_scheduled_date(self, scheduled_date: date) -> None:
        """Update the date this task occurrence is scheduled for."""
        self.scheduled_date = scheduled_date

    def is_done(self) -> bool:
        """Return whether the task has been completed."""
        return self.done

    def mark_done(self) -> None:
        """Mark the task as completed."""
        self.done = True

    def next_occurrence(self):
        """Return a fresh, not-done Task for this task's next occurrence, or None if not recurring.

        The clone keeps the same title/duration/priority/category/scheduled_time/recurrence,
        gets a new task_id, and advances scheduled_date by the recurrence frequency.
        """
        if self.recurring is None:
            return None
        clone = Task(
            title=self.title,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            category=self.category,
            recurring=self.recurring,
            scheduled_time=self.scheduled_time,
            scheduled_date=_advance_date(self.scheduled_date, self.recurring),
        )
        clone.pet_id = self.pet_id
        return clone


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
            "scheduled_time": task.set_scheduled_time,
        }
        for field, value in changes.items():
            if field not in setters:
                raise ValueError(f"Unknown task field: {field}")
            setters[field](value)

    def complete_task(self, task_id: str) -> None:
        """Mark one of this pet's tasks done, auto-scheduling its next occurrence if recurring."""
        task = self._find_task(task_id)
        if task is None:
            raise ValueError(f"No task with id {task_id} for pet {self.name}")
        task.mark_done()
        next_task = task.next_occurrence()
        if next_task is not None:
            self.add_task(next_task)

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


PRIORITY_WEIGHT = {"high": 1000, "medium": 100, "low": 10}
NEAR_MISS_MINUTES = 5


class Scheduler:
    def __init__(self, optimize_for_fit: bool = False):
        """Create a scheduler with no plan generated yet.

        optimize_for_fit=False (default) preserves strict priority order: higher-priority
        tasks always get scheduled first, even if that leaves time unused.
        optimize_for_fit=True instead maximizes total priority value packed into the
        available time (a 0/1 knapsack), which can leave a top task unscheduled if
        several lower-priority tasks fit better together.
        """
        self.planned = []
        self.skipped = []
        self.skip_shortfalls = {}
        self.optimize_for_fit = optimize_for_fit

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

    def sort_by_time(self, tasks: list) -> list:
        """Return tasks ordered by their scheduled time of day, earliest first.

        Tasks with no scheduled_time are treated as unscheduled and sort after all
        tasks that do have a time, in their original relative order.
        """
        return sorted(
            tasks,
            key=lambda task: (task.get_scheduled_time() is None, task.get_scheduled_time()),
        )

    def find_time_conflicts(self, pets: list) -> list:
        """Return groups of tasks that are scheduled at the exact same date and time.

        Tasks with no scheduled_time are ignored, since there's nothing to conflict on.
        Considers tasks across all given pets, so it catches conflicts both within a
        single pet's schedule and between different pets' tasks. Each group in the
        returned list is a list of two or more Task objects sharing a (date, time) slot.
        """
        tasks_by_slot = {}
        for task in self.get_all_tasks(pets):
            if task.get_scheduled_time() is None:
                continue
            slot = (task.get_scheduled_date(), task.get_scheduled_time())
            tasks_by_slot.setdefault(slot, []).append(task)

        return [tasks for tasks in tasks_by_slot.values() if len(tasks) > 1]

    def explain_conflicts(self, pets: list) -> list:
        """Return a warning message per detected scheduling conflict, instead of raising.

        This is a lightweight, non-fatal check: conflicting tasks are still valid data
        (find_time_conflicts never raises), this just renders them as readable warnings
        for display, e.g. in a UI banner or CLI print.
        """
        conflicts = self.find_time_conflicts(pets)
        warnings = []
        for group in conflicts:
            when = f"{group[0].get_scheduled_date()} at {group[0].get_scheduled_time().strftime('%H:%M')}"
            titles = ", ".join(task.get_title() for task in group)
            warnings.append(f"Warning: {len(group)} tasks scheduled for {when} — {titles}.")
        return warnings

    def filter_tasks(self, pets: list, done: bool = None, pet_name: str = None) -> list:
        """Return tasks across the given pets, optionally filtered by completion status and/or pet name.

        done=None or pet_name=None means that filter is not applied. pet_name matching is
        case-insensitive.
        """
        tasks = []
        for pet in pets:
            if pet_name is not None and pet.get_name().lower() != pet_name.lower():
                continue
            for task in pet.get_tasks():
                if done is not None and task.is_done() != done:
                    continue
                tasks.append(task)
        return tasks

    def _fit_greedy(self, tasks: list, minutes_available: int):
        """Fill the time budget strictly in priority order, skipping anything that doesn't fit."""
        ordered_tasks = self.sort_by_priority(tasks)
        planned, skipped = [], []
        remaining_minutes = minutes_available
        self.skip_shortfalls = {}
        for task in ordered_tasks:
            if task.get_duration() <= remaining_minutes:
                planned.append(task)
                remaining_minutes -= task.get_duration()
            else:
                skipped.append(task)
                self.skip_shortfalls[task.task_id] = task.get_duration() - remaining_minutes
        return planned, skipped

    def _fit_knapsack(self, tasks: list, minutes_available: int) -> tuple:
        """Choose the subset of tasks that maximizes total priority value within the time budget.

        Classic 0/1 knapsack (weight = duration, value = priority weight). This can pack more
        total care into the day than greedy-by-priority, at the cost of sometimes bumping a
        single high-priority task in favor of several lower-priority ones that fit better.

        Uses a 1D dp array instead of a full n x capacity table, since capacity (minutes
        available) is typically much larger than n (number of tasks) for this app. choice[c]
        tracks which tasks produced dp[c], so the best subset is available directly with no
        separate backtracking pass.

        Args:
            tasks: candidate tasks to choose from (not yet filtered or sorted).
            minutes_available: total time budget (the knapsack capacity), in minutes.

        Returns:
            A (planned, skipped) tuple: planned is the chosen subset sorted by priority,
            skipped is every other task. Also updates self.skip_shortfalls for skipped
            tasks that missed fitting by a small margin (see _explain_skip).
        """
        capacity = minutes_available
        dp = [0] * (capacity + 1)
        choice = [[] for _ in range(capacity + 1)]

        for task in tasks:
            duration = task.get_duration()
            value = PRIORITY_WEIGHT.get(task.get_priority(), 1)
            # Walk capacity backwards so each task is only ever considered once per pass;
            # a forward walk would let the same task be "reused" within one iteration.
            for c in range(capacity, duration - 1, -1):
                candidate_value = dp[c - duration] + value
                if candidate_value > dp[c]:
                    dp[c] = candidate_value
                    choice[c] = choice[c - duration] + [task]

        planned = choice[capacity]
        planned_ids = {task.task_id for task in planned}
        skipped = [task for task in tasks if task.task_id not in planned_ids]

        leftover_capacity = capacity - sum(task.get_duration() for task in planned)
        self.skip_shortfalls = {
            task.task_id: task.get_duration() - leftover_capacity
            for task in skipped
            if task.get_duration() > leftover_capacity
        }
        return self.sort_by_priority(planned), skipped

    def generate_plan(self, pets: list, minutes_available: int) -> list:
        """Build today's plan by fitting tasks into the time budget.

        Uses greedy priority-first fitting by default, or knapsack-based fitting
        (see self.optimize_for_fit) to maximize total priority value packed into the day.
        """
        active_tasks = [task for task in self.get_all_tasks(pets) if not task.is_done()]

        if self.optimize_for_fit:
            self.planned, self.skipped = self._fit_knapsack(active_tasks, minutes_available)
        else:
            self.planned, self.skipped = self._fit_greedy(active_tasks, minutes_available)

        return self.planned

    def explain_plan(self) -> str:
        """Return a human-readable explanation of which tasks were scheduled or skipped, and why."""
        if not self.planned and not self.skipped:
            return "No plan has been generated yet."

        lines = []
        for task in self.planned:
            lines.append(f"- {task.get_title()} ({task.get_duration()} min, {task.get_priority()} priority): scheduled.")
        for task in self.skipped:
            lines.append(self._explain_skip(task))
        return "\n".join(lines)

    def _explain_skip(self, task) -> str:
        """Explain why a single task was skipped, calling out near-misses distinctly."""
        prefix = f"- {task.get_title()} ({task.get_duration()} min, {task.get_priority()} priority): "
        over_by = getattr(self, "skip_shortfalls", {}).get(task.task_id)
        if over_by is not None and 0 < over_by <= NEAR_MISS_MINUTES:
            return prefix + f"skipped, missed by only {over_by} minute(s) — consider trimming another task."
        return prefix + "skipped, not enough time remaining."


class Owner:
    def __init__(self, name: str, age: int, dob: date, minutes_available: int):
        """Create a new owner with no pets yet and a dedicated Scheduler."""
        self.name = name
        self.age = age
        self.dob = dob
        self.minutes_available = minutes_available
        self.pets = []
        self.scheduler = Scheduler()

    def get_name(self) -> str:
        """Return the owner's name."""
        return self.name

    def set_name(self, name: str) -> None:
        """Update the owner's name."""
        self.name = name

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

    def set_optimize_for_fit(self, optimize_for_fit: bool) -> None:
        """Switch the scheduler between strict priority order and max-value knapsack fitting."""
        self.scheduler.optimize_for_fit = optimize_for_fit

    def get_optimize_for_fit(self) -> bool:
        """Return whether the scheduler is using knapsack-based fitting."""
        return self.scheduler.optimize_for_fit

    def filter_tasks(self, done: bool = None, pet_name: str = None) -> list:
        """Return this owner's tasks, optionally filtered by completion status and/or pet name."""
        return self.scheduler.filter_tasks(self.pets, done=done, pet_name=pet_name)

    def find_time_conflicts(self) -> list:
        """Return groups of this owner's tasks that are scheduled at the exact same date and time."""
        return self.scheduler.find_time_conflicts(self.pets)

    def explain_conflicts(self) -> list:
        """Return a warning message per detected scheduling conflict among this owner's tasks."""
        return self.scheduler.explain_conflicts(self.pets)

    def generate_plan(self) -> list:
        """Generate today's plan across all of this owner's pets."""
        return self.scheduler.generate_plan(self.pets, self.minutes_available)

    def explain_plan(self) -> str:
        """Explain the most recently generated plan."""
        return self.scheduler.explain_plan()
