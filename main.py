# main.py
import streamlit as st

st.set_page_config(page_title="Pixel ToDo Gamifier", page_icon="🎮", layout="centered")

from components.styles import inject_custom_css
from components.auth import get_supabase_client, sign_in, sign_out
from components.tasks import init_task_state, add_task, display_tasks
from components.rewards import display_rewards
from components.constants import CATEGORIES, LEVELS_XP, SUBCATEGORIES_MAP

st.markdown(inject_custom_css(), unsafe_allow_html=True)

supabase = get_supabase_client()

if "user" not in st.session_state:
    st.session_state.user = None

# CATEGORIES = ["school", "work", "internship", "life", "study"]
# LEVELS_XP = {
#     "general": 10,
#     "easy": 20,
#     "medium": 30,
#     "difficult": 40,
#     "extreme": 50
# }

# SUBCATEGORIES_MAP = {
#     "school": ["homework", "projects", "exams"],
#     "work": ["meetings", "reports", "emails"],
#     "internship": ["tasks", "learning", "networking"],
#     "life": ["exercise", "chores", "hobbies"],
#     "study": ["reading", "practice", "review"]
# }

def login():
    st.title("🎮 Pixel ToDo Gamifier - Login")
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Sign In")
        if submitted:
            response = sign_in(email, password)
            if response.user:
                st.session_state.user = response.user
                st.success(f"Welcome, {response.user.email}!")
                st.rerun()
            else:
                st.error("Login failed. Check credentials.")


def logout():
    if st.button("Logout"):
        sign_out()
        st.session_state.user = None
        st.rerun()

def main_app():
    st.title("🎮 Pixel ToDo Gamifier")
    logout()

    init_task_state()

    with st.sidebar:
        st.header("Add New Task")

        # Category options with emojis
        category_options = [
            f"{cat}" if cat=="COLLEGE" else
            f"{cat}" if cat=="WORK" else
            f"{cat}" if cat=="INTERN" else
            f"{cat}" if cat=="STUDY" else
            f"{cat}" if cat=="LIFE" else
            f"{cat}" for cat in CATEGORIES
        ]
        selected_cat_label = st.segmented_control("Category", options=category_options)
        selected_category = selected_cat_label

        with st.form("add_task_form", clear_on_submit=True):
            # Category segmented control with emojis

            # Dynamic subcategory multiselect
            subcategories = SUBCATEGORIES_MAP.get(selected_category, [])
            selected_subcategories = st.multiselect("Subcategory (select one or more)", subcategories)

            # Task name input
            task_name = st.text_input("Task Name", max_chars=50)

            # Task difficulty level
            task_level = st.selectbox("Level", list(LEVELS_XP.keys()))
            
            submitted = st.form_submit_button("Add Task")

            if submitted:
                if not task_name.strip():
                    st.warning("Task name cannot be empty!")
                elif not selected_subcategories:
                    st.warning("Select at least one subcategory!")
                else:
                    add_task(task_name.strip(), selected_category, selected_subcategories, task_level)
                    st.success(f"Task '{task_name.strip()}' added successfully under {selected_category} - {', '.join(selected_subcategories)} at {task_level} level.")

    tab1, tab2 = st.tabs(["Tasks", "Rewards"])

    with tab1:
        display_tasks()

    with tab2:
        display_rewards()

    st.markdown("""
    <footer>
        <p>✨ Stay productive & level up your life! ✨</p>
    </footer>
    """, unsafe_allow_html=True)


if st.session_state.user:
    main_app()
else:
    login()
