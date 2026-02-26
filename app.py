
import streamlit as st
import json
from pathlib import Path
import random
import string

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Digital Banking System",
    page_icon="🏦",
    layout="centered"
)

DATABASE = "data.json"

# ---------------- LOAD DATA ----------------
if Path(DATABASE).exists():
    with open(DATABASE, "r") as f:
        data = json.load(f)
else:
    data = []
    with open(DATABASE, "w") as f:
        json.dump(data, f)

def save_data():
    with open(DATABASE, "w") as f:
        json.dump(data, f, indent=4)

def generate_account():
    while True:
        acc = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        if not any(user["accountno"] == acc for user in data):
            return acc

# ---------------- HEADER ----------------
st.markdown("<h1 style='text-align:center;'>🏦 Digital Banking System</h1>", unsafe_allow_html=True)
st.markdown("---")

# ---------------- SIDEBAR ----------------
menu = st.sidebar.radio(
    "📌 Navigation",
    ["🆕 Create Account", "💰 Deposit", "💸 Withdraw", "📄 View Details", "🗑 Delete Account"]
)

# ================= CREATE ACCOUNT =================
if menu == "🆕 Create Account":
    st.subheader("🆕 Open New Account")

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("👤 Name")
        age = st.number_input("🎂 Age", min_value=1)

    with col2:
        email = st.text_input("📧 Email")
        phone = st.text_input("📱 Phone")

    pin = st.text_input("🔐 4 Digit PIN", type="password")

    if st.button("🚀 Create Account"):
        if age < 18:
            st.error("❌ Age must be 18+")
        elif not (phone.isdigit() and len(phone) == 10):
            st.error("❌ Invalid phone number")
        elif not (pin.isdigit() and len(pin) == 4):
            st.error("❌ Invalid PIN")
        else:
            account = generate_account()
            user = {
                "name": name,
                "age": age,
                "email": email,
                "phone": phone,
                "pin": pin,
                "accountno": account,
                "balance": 0
            }
            data.append(user)
            save_data()

            st.success("✅ Account Created Successfully!")
            st.info(f"🏦 Your Account Number: **{account}**")

# ================= DEPOSIT =================
elif menu == "💰 Deposit":
    st.subheader("💰 Deposit Money")

    acc = st.text_input("🏦 Account Number")
    pin = st.text_input("🔐 PIN", type="password")
    amount = st.number_input("💵 Amount", min_value=0)

    if st.button("➕ Deposit"):
        user = next((u for u in data if u["accountno"] == acc and u["pin"] == pin), None)

        if not user:
            st.error("❌ User not found")
        else:
            user["balance"] += amount
            save_data()
            st.success("✅ Amount Deposited Successfully")

# ================= WITHDRAW =================
elif menu == "💸 Withdraw":
    st.subheader("💸 Withdraw Money")

    acc = st.text_input("🏦 Account Number")
    pin = st.text_input("🔐 PIN", type="password")
    amount = st.number_input("💵 Amount", min_value=0)

    if st.button("➖ Withdraw"):
        user = next((u for u in data if u["accountno"] == acc and u["pin"] == pin), None)

        if not user:
            st.error("❌ User not found")
        elif user["balance"] < amount:
            st.error("❌ Insufficient Balance")
        else:
            user["balance"] -= amount
            save_data()
            st.success("✅ Amount Withdrawn Successfully")

# ================= VIEW DETAILS =================
elif menu == "📄 View Details":
    st.subheader("📄 Account Details")

    acc = st.text_input("🏦 Account Number")
    pin = st.text_input("🔐 PIN", type="password")

    if st.button("🔍 Show Details"):
        user = next((u for u in data if u["accountno"] == acc and u["pin"] == pin), None)

        if not user:
            st.error("❌ User not found")
        else:
            st.markdown("### 👤 Customer Information")
            st.write("**Name:**", user["name"])
            st.write("**Email:**", user["email"])
            st.write("**Phone:**", user["phone"])
            st.markdown("---")
            st.markdown(f"## 💰 Current Balance: ₹ {user['balance']}")

# ================= DELETE =================
elif menu == "🗑 Delete Account":
    st.subheader("🗑 Delete Account")

    acc = st.text_input("🏦 Account Number")
    pin = st.text_input("🔐 PIN", type="password")

    if st.button("⚠ Delete Account"):
        user = next((u for u in data if u["accountno"] == acc and u["pin"] == pin), None)

        if not user:
            st.error("❌ User not found")
        else:
            data.remove(user)
            save_data()
            st.success("✅ Account Deleted Successfully")