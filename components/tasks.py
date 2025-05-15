import streamlit as st
from .constants import CATEGORIES, LEVELS_XP, SUBCATEGORIES_MAP

from datetime import datetime, date

def init_task_state(user_id, supabase_client):
    if "xp" not in st.session_state:
        st.session_state.xp = 0
    if "coins" not in st.session_state:
        st.session_state.coins = 0

    # Fetch tasks from DB for the user where done=False
    response = supabase_client.table("tasks").select("*").eq("user_id", user_id).eq("done", False).execute()
    if not response:
        st.error(f"Error fetching tasks: {response.data}")
        st.session_state.tasks = []
    else:
        tasks = response.data
        for task in tasks:
            if "due_date" in task and task["due_date"]:
                task["due_date"] = datetime.strptime(task["due_date"], "%Y-%m-%d").date()
            else:
                task["due_date"] = None
        st.session_state.tasks = tasks


def calculate_level(xp):
    return xp // 100 + 1



def add_task(name, category, subcategories, level, due_date):
    task = {
        "name": name,
        "category": category,
        "subcategories": subcategories,
        "level": level,
        "xp": LEVELS_XP[level],
        "done": False,
        "due_date": due_date,  # store the date here (datetime.date)
    }
    response = supabase_client.table("tasks").insert(task).execute()

    if response.error:
        st.error(f"Failed to add task: {response.error.message}")
    else:
        # Also add locally to session state
        st.session_state.tasks.append(task)
        st.success(f"Task '{name}' added successfully!")

def display_tasks():
    st.header(f"Your Tasks - Level {calculate_level(st.session_state.xp)} | XP: {st.session_state.xp} | Coins: {st.session_state.coins} 🪙")

    if len(st.session_state.tasks) == 0:
        st.info("No tasks added yet! Use the sidebar to add some.")
        return

    # Filter and sort tasks by due_date ascending (only undone tasks)
    undone_tasks = [t for t in st.session_state.tasks if not t["done"]]
    undone_tasks.sort(key=lambda x: x["due_date"] or datetime.max.date())

    data = []
    for i, task in enumerate(undone_tasks):
        data.append({
            "Task Name": task["name"],
            "Category": task["category"].title(),
            "Subcategories": ", ".join(task["subcategories"]),
            "Level": task["level"].capitalize(),
            "XP": task["xp"],
            "Due Date": task["due_date"].strftime("%Y-%m-%d") if task["due_date"] else "No due date",
            "Done": task["done"],
            "_idx": st.session_state.tasks.index(task)  # map back to original index
        })

    if not data:
        st.success("All tasks completed! 🎉")
        return

    df = pd.DataFrame(data)
    edited_df = st.data_editor(
        df.drop(columns=["_idx"]),
        column_config={
            "Task Name": st.column_config.TextColumn("Task Name"),
            "Category": st.column_config.TextColumn("Category"),
            "Subcategories": st.column_config.TextColumn("Subcategories"),
            "Level": st.column_config.TextColumn("Level"),
            "XP": st.column_config.NumberColumn("XP"),
            "Due Date": st.column_config.TextColumn("Due Date"),
            "Done": st.column_config.CheckboxColumn("Done"),
        },
        disabled=["Task Name", "Category", "Subcategories", "Level", "XP", "Due Date"],
        hide_index=True,
        key="tasks_data_editor"
    )

    for i, row in edited_df.iterrows():
        orig_idx = df.iloc[i]["_idx"]
        if row["Done"] and not st.session_state.tasks[orig_idx]["done"]:
            st.session_state.tasks[orig_idx]["done"] = True
            st.session_state.tasks[orig_idx]["completed_date"] = datetime.today().date()
            mark_done(orig_idx)


    # Show collapsible section
    # done_tasks = [t for t in st.session_state.tasks if t["done"]]
    # if done_tasks:
    #     st.markdown("<details><summary style='color:#00fff7; cursor:pointer;'>Completed Tasks</summary>", unsafe_allow_html=True)
    #     for t in done_tasks:
    #         st.markdown(f"- {t['name']} ({t['level'].capitalize()} - {t['xp']} XP)")
    #     st.markdown("</details>", unsafe_allow_html=True)


def add_task_form():
    st.sidebar.header("Add New Task")

    category_options = [
            f"{cat}" if cat=="COLLEGE" else
            f"{cat}" if cat=="WORK" else
            f"{cat}" if cat=="INTERN" else
            f"{cat}" if cat=="STUDY" else
            f"{cat}" if cat=="LIFE" else
            f"{cat}" for cat in CATEGORIES
        ]

    selected_cat_label = st.sidebar.segmented_control("Category", category_options)
    selected_category = selected_cat_label

    subcategories = SUBCATEGORIES_MAP.get(selected_category, [])
    selected_subcategories = st.sidebar.multiselect("Subcategory (select one or more)", subcategories)

    task_name = st.sidebar.text_input("Task Name", max_chars=50)

    level = st.sidebar.selectbox("Level", list(LEVELS_XP.keys()))

    if st.sidebar.button("Add Task"):
        if not task_name.strip():
            st.sidebar.warning("Task name cannot be empty!")
        elif not selected_subcategories:
            st.sidebar.warning("Select at least one subcategory!")
        else:
            add_task(task_name.strip(), selected_category, selected_subcategories, level)
            st.sidebar.success(f"Task '{task_name}' added under {selected_category} - {', '.join(selected_subcategories)} at {level} level.")
