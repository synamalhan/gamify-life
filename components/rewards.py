# components/rewards.py
import streamlit as st

REWARDS = {
    "Coffee Break ☕ (10 coins)": 10,
    "15 min Game Time 🎮 (20 coins)": 20,
    "Snack Time 🍪 (30 coins)": 30,
    "Watch an Episode 📺 (50 coins)": 50,
    "Buy a Treat 🎁 (100 coins)": 100
}

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
