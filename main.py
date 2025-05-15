# main.py
import streamlit as st

st.set_page_config(page_title="Pixel ToDo Gamifier", layout="centered")

from components.styles import inject_custom_css
from components.auth import get_supabase_client, sign_in, sign_out
from components.tasks import init_task_state, add_task, display_tasks
from components.rewards import display_rewards
from components.analytics import display_analytics
from components.constants import CATEGORIES, LEVELS_XP, SUBCATEGORIES_MAP

# st.markdown(inject_custom_css(), unsafe_allow_html=True)

supabase = get_supabase_client()

if "user" not in st.session_state:
    st.session_state.user = None
    
from datetime import datetime, date


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

    # Load user tasks from DB
    init_task_state(st.session_state.user.id, supabase)

    with st.sidebar:
        st.header("Add New Task")

        category_options = CATEGORIES
        selected_category = st.segmented_control("Category", options=category_options)

        with st.form("add_task_form", clear_on_submit=True):
            subcategories = SUBCATEGORIES_MAP.get(selected_category, [])
            selected_subcategories = st.multiselect("Subcategory (select one or more)", subcategories)
            task_name = st.text_input("Task Name", max_chars=50)
            task_level = st.selectbox("Level", list(LEVELS_XP.keys()))
            due_date = st.date_input("Due Date", value=None)
            submitted = st.form_submit_button("Add Task")

            if submitted:
                if not task_name.strip():
                    st.warning("Task name cannot be empty!")
                elif not selected_subcategories:
                    st.warning("Select at least one subcategory!")
                else:
                    add_task(task_name.strip(), selected_category, selected_subcategories, task_level, due_date, st.session_state.user.id, supabase)
                    st.success(f"Task '{task_name.strip()}' added successfully under {selected_category} - {', '.join(selected_subcategories)} at {task_level} level.")

    tab1, tab2, tab3= st.tabs(["Tasks", "Rewards", "Analytics"])

    with tab1:
        display_tasks()

    with tab2:
        display_rewards()

    with tab3:
        display_analytics()

    st.markdown("""
    <footer>
        <p>✨ Stay productive & level up your life! ✨</p>
    </footer>
    """, unsafe_allow_html=True)


if st.session_state.user:
    main_app()
else:
    login()
