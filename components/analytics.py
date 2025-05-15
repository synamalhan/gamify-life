import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime


def display_analytics():
    st.header("📊 Productivity Analytics")

    tasks = st.session_state.get("tasks", [])
    if not tasks:
        st.info("No tasks to analyze yet.")
        return

    # Get completed tasks
    completed_tasks = [
        {**task, "completed_date": task.get("completed_date", datetime.today().date())}
        for task in tasks if task["done"]
    ]

    if not completed_tasks:
        st.success("No tasks completed yet! Start ticking some off. ✅")
        return

    df = pd.DataFrame(completed_tasks)
    df["completed_date"] = pd.to_datetime(df["completed_date"]).dt.date

    # -----------------------------
    # 1. Bar Chart: Tasks per Level per Day
    # -----------------------------
    st.subheader("📅 Daily Task Completions by Level")

    daily_level_df = df.groupby(["completed_date", "level"]).size().reset_index(name="count")

    chart = alt.Chart(daily_level_df).mark_bar().encode(
        x=alt.X("completed_date:T", title="Date"),
        y=alt.Y("count:Q", title="Tasks Completed"),
        color=alt.Color("level:N", title="Level"),
        tooltip=["completed_date", "level", "count"]
    ).properties(height=400)

    st.altair_chart(chart, use_container_width=True)

    col1, col2 = st.columns(2)

    # -----------------------------
    # 2. Table: Level-wise Task Completions
    # -----------------------------
    col1.subheader("📘 Tasks Completed Per Level")

    level_summary = df["level"].value_counts().rename_axis("Level").reset_index(name="Tasks Completed")
    col1.dataframe(level_summary, use_container_width=True, hide_index=True)

    # -----------------------------
    # 3. Table: Category-wise Task Completions
    # -----------------------------
    col2.subheader("📂 Tasks Completed Per Category")

    category_summary = df["category"].value_counts().rename_axis("Category").reset_index(name="Tasks Completed")
    col2.dataframe(category_summary, use_container_width=True, hide_index=True)

    # -----------------------------
    # 4. Expander: Completed Task Details (at bottom)
    # -----------------------------
    st.markdown("---")
    with st.expander("📜 View Completed Tasks in Detail"):
        detailed_df = df[["name", "category", "subcategories", "level", "xp", "completed_date"]].copy()
        detailed_df["Done"] = True  # Add Done checkbox column as always True
        detailed_df = detailed_df.rename(columns={
            "name": "Task Name",
            "category": "Category",
            "subcategories": "Subcategories",
            "level": "Level",
            "xp": "XP",
            "completed_date": "Completed On"
        })
        st.data_editor(
            detailed_df,
            column_config={
                "Task Name": st.column_config.TextColumn(),
                "Category": st.column_config.TextColumn(),
                "Subcategories": st.column_config.TextColumn(),
                "Level": st.column_config.TextColumn(),
                "XP": st.column_config.NumberColumn(),
                "Completed On": st.column_config.DateColumn(),
                "Done": st.column_config.CheckboxColumn("Done")
            },
            disabled=["Task Name", "Category", "Subcategories", "Level", "XP", "Completed On", "Done"],
            use_container_width=True,
            hide_index=True
        )
