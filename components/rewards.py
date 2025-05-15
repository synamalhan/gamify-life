# components/rewards.py
import streamlit as st
from .constants import REWARDS


def spend_coins(cost):
    if st.session_state.coins >= cost:
        st.session_state.coins -= cost
        st.success("Reward redeemed! Enjoy your reward!")
    else:
        st.error("Not enough coins to redeem this reward.")

def display_rewards():
    st.header("Rewards Shop")
    st.write("Spend your coins 🪙 to redeem rewards!")
    for reward, cost in REWARDS.items():
        if st.button(f"{reward} - Cost: {cost} coins", key=f"reward_{reward}"):
            spend_coins(cost)

    st.markdown("---")
    st.write("Your coins:", st.session_state.coins)
