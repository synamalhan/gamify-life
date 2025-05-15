# components/auth.py
from supabase import create_client
import streamlit as st

def get_supabase_client():
    url = st.secrets["url"]
    key = st.secrets["key"]
    return create_client(url, key)

def sign_in(email, password):
    supabase = get_supabase_client()
    user = supabase.auth.sign_in_with_password({"email": email, "password": password})
    return user

def sign_up(email, password):
    supabase = get_supabase_client()
    user = supabase.auth.sign_up({"email": email, "password": password})
    return user

def sign_out():
    supabase = get_supabase_client()
    supabase.auth.sign_out()
    st.session_state.pop("user", None)
