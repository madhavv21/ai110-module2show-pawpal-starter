"""PawPal+ class skeleton, generated from diagrams/uml.mmd. No logic yet."""


class Pet:
    def __init__(self, name: str, species: str, breed: str, age: int):
        self.name = name
        self.species = species
        self.breed = breed
        self.age = age

    def get_name(self) -> str:
        raise NotImplementedError

    def set_name(self, name: str) -> None:
        raise NotImplementedError

    def get_species(self) -> str:
        raise NotImplementedError

    def describe(self) -> str:
        raise NotImplementedError


class Task:
    def __init__(self, title: str, duration_minutes: int, priority: str, category: str, recurring: bool):
        self.title = title
        self.duration_minutes = duration_minutes
        self.priority = priority
        self.category = category
        self.recurring = recurring

    def get_title(self) -> str:
        raise NotImplementedError

    def get_duration(self) -> int:
        raise NotImplementedError

    def set_duration(self, minutes: int) -> None:
        raise NotImplementedError

    def get_priority(self) -> str:
        raise NotImplementedError

    def set_priority(self, priority: str) -> None:
        raise NotImplementedError

    def is_recurring(self) -> bool:
        raise NotImplementedError


class Schedule:
    def __init__(self):
        self.tasks = []
        self.planned = []
        self.skipped = []

    def add_task(self, task: Task) -> None:
        raise NotImplementedError

    def edit_task(self, title: str, changes: dict) -> None:
        raise NotImplementedError

    def remove_task(self, title: str) -> None:
        raise NotImplementedError

    def sort_by_priority(self) -> list:
        raise NotImplementedError

    def generate_plan(self, minutes_available: int) -> list:
        raise NotImplementedError

    def explain_plan(self) -> str:
        raise NotImplementedError


class User:
    def __init__(self, name: str, age: int, dob, minutes_available: int):
        self.name = name
        self.age = age
        self.dob = dob
        self.minutes_available = minutes_available
        self.pet = None
        self.schedule = Schedule()

    def set_pet(self, pet: Pet) -> None:
        raise NotImplementedError

    def get_pet(self) -> Pet:
        raise NotImplementedError

    def get_minutes_available(self) -> int:
        raise NotImplementedError

    def set_minutes_available(self, minutes: int) -> None:
        raise NotImplementedError
