# alerts.py
import streamlit as st
import json
import os

ALERTS_FILE = "alerts.json"

def load_alerts():
    if os.path.exists(ALERTS_FILE):
        with open(ALERTS_FILE, "r") as f:
            return json.load(f)
    return []

def save_alerts(alerts):
    with open(ALERTS_FILE, "w") as f:
        json.dump(alerts, f, indent=4)

def alert_form_ui():
    st.title("⚡ Set Price Alerts for Stocks & Crypto")

    with st.form("alert_form"):
        symbol = st.text_input("Symbol (e.g., AAPL or BTC)").strip().upper()
        market = st.radio("Market Type", ["Stock", "Crypto"], horizontal=True)
        alert_type = st.selectbox("Alert Type", ["Price goes ABOVE", "Price goes BELOW"])
        target_price = st.number_input("Target Price (USD)", min_value=0.0, format="%.2f")
        contact_method = st.radio("Notify via", ["Email", "SMS"], horizontal=True)
        contact = st.text_input(f"Your {contact_method} address or phone number").strip()

        submitted = st.form_submit_button("Save Alert")

    if submitted:
        if not symbol:
            st.error("Please enter a symbol.")
        elif not contact:
            st.error(f"Please enter your {contact_method}.")
        else:
            if market == "Crypto" and not symbol.endswith("-USD"):
                symbol = symbol + "-USD"
            alerts = load_alerts()
            alert = {
                "symbol": symbol,
                "market": market,
                "alert_type": alert_type,
                "target_price": target_price,
                "contact_method": contact_method,
                "contact": contact
            }
            alerts.append(alert)
            save_alerts(alerts)
            st.success(f"Alert for {symbol} at ${target_price} saved! You'll be notified via {contact_method}.")

            if __name__ == "__main__":
    alert_form_ui()