from supabase import create_client
import streamlit as st

# Get secrets from .streamlit/secrets.toml
url = st.secrets["url"]
key = st.secrets["key"]

supabase = create_client(url, key)
