import streamlit as st
import base64
import os

# @st.cache_data(show_spinner=False)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = f'''
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
'''
    if (page_bg_img):
        st.markdown(page_bg_img, unsafe_allow_html=True)
   

def inject_custom_css():
    css = """
    <style>
    body, .block-container {
        font-family: "Courier New", Courier, monospace;
        color: #f0f0f0;
        min-height: 100vh;
        margin: 0;
    }
    h1 {
        color: #ffffff;
        text-shadow: 0 0 4px #ffffff, 0 0 8px #ffffff;
    }
    h2 {
        color: #ffffff;
        text-shadow: 0 0 3px #ffffff, 0 0 6px #ffffff;
    }
    h3 {
        color: #ffffff;
        text-shadow: 0 0 2px #ffffff, 0 0 4px #ffffff;
    }
    p, label, span, li, .stText, .stMarkdown {
        color: #e0e0e0;
    }
    .stButton > button {
        background: #ffffff;
        color: #202020;
        border-radius: 8px;
        border: none;
        padding: 8px;
        font-weight: bold;
        cursor: pointer;
        box-shadow: none;
        transition: 0.3s;
    }
    .stButton > button:hover {
        background: #f0f0f0;
        color: #101010;
        box-shadow: none;
    }
    .stTextInput > div > input,
    .stSelectbox > div > div > select {
        background: #202020;
        border: 2px solid #ffffff;
        border-radius: 6px;
        color: #ffffff;
        font-weight: bold;
        font-family: "Courier New", Courier, monospace;
        font-size: 12px;
        padding: 6px 8px;
        box-shadow: none;
    }
    .pixel-box {
        background: rgba(255, 255, 255, 0.15);
        border: 2px solid #ffffff;
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 8px;
        font-size: 14px;
        color: #e0e0e0;
    }
    .task-done {
        text-decoration: line-through;
        color: #606060;
        opacity: 0.7;
    }
    .reward-btn {
        background: #ffd994;
        color: #332a00;
        font-weight: bold;
        border: 2px solid #332a00;
        border-radius: 8px;
        padding: 8px;
        width: 100%;
        margin-bottom: 8px;
        cursor: pointer;
        box-shadow: none;
        transition: 0.3s;
    }
    .reward-btn:hover {
        background: #e6c573;
        color: #332a00;
        box-shadow: none;
    }
    footer {
        text-align: center;
        margin-top: 24px;
        font-size: 12px;
        color: #ffffff;
    }
    .logout-button-container {
        position: fixed;
        top: 16px;
        right: 16px;
        z-index: 100;
    }
    .logout-button-container .stButton > button {
        background: #ff6c93;
        color: #202020;
        border-radius: 8px;
        border: none;
        padding: 6px 12px;
        font-weight: bold;
        cursor: pointer;
        box-shadow: none;
        transition: 0.3s;
    }
    .logout-button-container .stButton > button:hover {
        background: #b281ff;
        color: #101010;
        box-shadow: none;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


# Get the absolute path to your background image relative to this file
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKGROUND_PATH = os.path.join(BASE_DIR, '..', 'assets', 'background.png')
if not os.path.exists(BACKGROUND_PATH):
    st.error(f"Image not found at: {BACKGROUND_PATH}")

set_png_as_page_bg(BACKGROUND_PATH)
inject_custom_css()
