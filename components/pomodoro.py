import streamlit as st
import time

def display_pomodoro_timer():
    st.header("🍅 Pomodoro Timer", anchor=False)

    # Initialize session state
    if "pomo_running" not in st.session_state:
        st.session_state.pomo_running = False
        st.session_state.pomo_start_time = None
        st.session_state.pomo_duration = 25 * 60  # in seconds

    # Calculate remaining time
    remaining = 0
    if st.session_state.pomo_running:
        elapsed = time.time() - st.session_state.pomo_start_time
        remaining = max(0, st.session_state.pomo_duration - elapsed)
        if remaining <= 0:
            st.success("Pomodoro complete! 🎉")
            st.session_state.pomo_running = False

    # Centered timer box (shown before slider)
    with st.container():
        st.markdown(
            f"""
            <div style='display: flex; justify-content: center; align-items: center; padding: 20px;'>
                <div style='background-color: white; color: black; font-size: 48px;
                            font-weight: bold; padding: 30px 60px; border-radius: 12px;
                            box-shadow: 0px 4px 12px rgba(0,0,0,0.1);'>
                    {f"{int(remaining // 60):02d}:{int(remaining % 60):02d}" if st.session_state.pomo_running else "00:00"}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Duration slider
    duration_min = st.slider("Set Pomodoro Duration (minutes)", 10, 60, 25)

    # Control buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("▶️ Start Pomodoro"):
            st.session_state.pomo_duration = duration_min * 60
            st.session_state.pomo_start_time = time.time()
            st.session_state.pomo_running = True

    with col2:
        if st.button("⏹️ Reset Timer"):
            st.session_state.pomo_running = False
            st.session_state.pomo_start_time = None
