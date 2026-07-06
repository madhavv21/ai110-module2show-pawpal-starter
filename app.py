from datetime import date

import streamlit as st

from pawpal_system import Owner, Pet, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time and priority, and explains why it
chose the plan it did.
"""
)

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="", age=0, dob=date.today(), minutes_available=60)

owner = st.session_state.owner

st.divider()
st.subheader("Owner Info")

col1, col2, col3 = st.columns(3)
with col1:
    owner.set_name(st.text_input("Owner name", value=owner.get_name()))
with col2:
    owner.age = st.number_input("Owner age", min_value=0, max_value=120, value=owner.age)
with col3:
    minutes = st.number_input(
        "Minutes available today", min_value=0, max_value=600, value=owner.get_minutes_available()
    )
    owner.set_minutes_available(int(minutes))

st.divider()
st.subheader("Pets")

with st.form("add_pet_form", clear_on_submit=True):
    st.caption("Add a pet before adding tasks for it.")
    pcol1, pcol2, pcol3, pcol4 = st.columns(4)
    with pcol1:
        new_pet_name = st.text_input("Pet name", value="")
    with pcol2:
        new_pet_species = st.selectbox("Species", ["dog", "cat", "other"])
    with pcol3:
        new_pet_breed = st.text_input("Breed", value="")
    with pcol4:
        new_pet_age = st.number_input("Pet age", min_value=0, max_value=40, value=0)

    if st.form_submit_button("Add pet") and new_pet_name:
        owner.add_pet(Pet(new_pet_name, new_pet_species, new_pet_breed, int(new_pet_age)))

pets = owner.get_pets()

if not pets:
    st.info("No pets yet. Add one above.")
else:
    for pet in pets:
        with st.expander(pet.describe(), expanded=False):
            if st.button("Remove pet", key=f"remove_pet_{pet.pet_id}"):
                owner.remove_pet(pet.pet_id)
                st.rerun()

st.divider()
st.subheader("Tasks")

if not pets:
    st.info("Add a pet before adding tasks.")
else:
    pet_by_name = {pet.get_name(): pet for pet in pets}
    selected_pet_name = st.selectbox("Which pet is this task for?", list(pet_by_name.keys()))
    selected_pet = pet_by_name[selected_pet_name]

    with st.form("add_task_form", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            task_title = st.text_input("Task title", value="")
        with col2:
            duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
        with col3:
            priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

        col4, col5 = st.columns(2)
        with col4:
            category = st.text_input("Category", value="general")
        with col5:
            recurring_choice = st.selectbox("Recurring", ["None", "daily", "weekly", "monthly"])
            recurring = None if recurring_choice == "None" else recurring_choice

        if st.form_submit_button("Add task") and task_title:
            selected_pet.add_task(Task(task_title, int(duration), priority, category, recurring))

    tasks = selected_pet.get_tasks()
    if not tasks:
        st.info(f"No tasks yet for {selected_pet.get_name()}.")
    else:
        st.write(f"Tasks for {selected_pet.get_name()}:")
        for task in tasks:
            tcol1, tcol2, tcol3 = st.columns([3, 1, 1])
            with tcol1:
                status = "done" if task.is_done() else "not done"
                recurring_label = f", recurs {task.get_recurrence_frequency()}" if task.is_recurring() else ""
                st.write(
                    f"**{task.get_title()}** — {task.get_duration()} min, {task.get_priority()} priority "
                    f"({status}{recurring_label})"
                )
            with tcol2:
                if not task.is_done() and st.button("Mark done", key=f"done_{task.task_id}"):
                    selected_pet.complete_task(task.task_id)
                    st.rerun()
            with tcol3:
                if st.button("Remove", key=f"remove_task_{task.task_id}"):
                    selected_pet.remove_task(task.task_id)
                    st.rerun()

st.divider()
st.subheader("Build Schedule")

optimize_for_fit = st.checkbox(
    "Maximize total tasks completed (may bump a single high-priority task for several smaller ones)",
    value=owner.get_optimize_for_fit(),
    help="Off: always schedule the highest-priority tasks first, even if time is left unused. "
    "On: pack the schedule to fit as much total priority value into the day as possible.",
)
owner.set_optimize_for_fit(optimize_for_fit)

for warning in owner.explain_conflicts():
    st.warning(warning)

if st.button("Generate schedule"):
    st.session_state.plan = owner.generate_plan()
    st.session_state.explanation = owner.explain_plan()

if "plan" in st.session_state:
    pets_by_id = {pet.pet_id: pet for pet in owner.get_pets()}

    st.markdown("### Today's Schedule")
    if not st.session_state.plan:
        st.info("No tasks fit today's plan.")
    else:
        for task in st.session_state.plan:
            pet = pets_by_id.get(task.pet_id)
            pet_label = pet.get_name() if pet else "Unknown pet"
            st.write(f"- **{pet_label}**: {task.get_title()} ({task.get_duration()} min) [priority: {task.get_priority()}]")

    st.markdown("### Why this plan")
    st.text(st.session_state.explanation)
