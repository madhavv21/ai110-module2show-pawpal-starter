# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

Today's Schedule
========================================
Mochi: Feeding (10 min) [priority: high]
Biscuit: Morning walk (30 min) [priority: high]
Mochi: Litter box cleaning (15 min) [priority: medium]

Why this plan:
- Feeding (10 min, high priority): scheduled.
- Morning walk (30 min, high priority): scheduled.
- Litter box cleaning (15 min, medium priority): scheduled.
- Grooming (45 min, low priority): skipped, not enough time remaining.

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
Command: python -m pytest

platform darwin -- Python 3.14.5, pytest-9.0.3, pluggy-1.6.0
rootdir: /Users/mverma/AI 110/ai110-module2show-pawpal-starter
plugins: anyio-4.13.0
collected 14 items

tests/test_pawpal.py ..............                                                                                                                                                                [100%]

=========================================================================================== 14 passed in 0.02s ===========================================================================================
```

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|

Task Sorting:
-Method(s): Scheduler.sort_by_priority(), Scheduler.sort_by_time()
-Sorts by high, medium, and low priority tiers or by the tasks' scheduled time

Filtering:
-Method(s): Scheduler.filter_tasks(), Owner.filter_tasks()
-Tasks filtered by completion status and/or pet name

Conflict Handling:
-Method(s): Scheduler.find_time_conflicts(), Scheduler.explain_conflicts(), Owner.find_time_conflicts(), Owner.explain_conflicts()
-Detects tasks scheduled at the same time across all pets and raises conflict warning messages

Recurring Tasks:
-Method(s): Task.next_occurrence(), Pet.complete_task()
-Based on the .recurring attribute, we can determine next occurence and then reschedule based on it

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. Owner types their name, age, and minutes available today
    Eg: Name: Madhav, Age: 19, Minutes available today: 180
2. Owner adds a pet, chooses their name, their breed, the species, and its age
    Eg: Pet name: Coco, Species: dog, Breed: Labrador, Pet age: 2
3. Owner adds a task, which means giving it a title, setting a duration, determining its priority, choosing a category to place it in, and selecting whether its recurring or not.
    Eg: Task Title: Walk, Duration: 40, Priority: medium, Category: Fitness, Recurring: daily
4. Owner can click "Mark Done" or "Remove" as needed for this particular task.
5. Owner can also generate a possible schedule for themselves, where they can also choose to maximize total tasks completed, but that may bump a single high-priority task for several smaller ones.

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
