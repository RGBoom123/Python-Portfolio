import json
import os
import yfinance as yf

def send_email(to_email, subject, body, from_email="your_email@gmail.com", password="your_app_password"):
    import smtplib
    from email.message import EmailMessage

    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(from_email, password)
    server.send_message(msg)
    server.quit()

# 👇 The rest of your alert checker follows...
def load_alerts():
    ...

def send_notification(alert, current_price):
    ...
    send_email(contact, f"Price Alert: {symbol}", message)

ALERTS_FILE = "alerts.json"

def load_alerts():
    if os.path.exists(ALERTS_FILE):
        with open(ALERTS_FILE, "r") as f:
            return json.load(f)
    return []

def save_alerts(alerts):
    with open(ALERTS_FILE, "w") as f:
        json.dump(alerts, f, indent=4)

def send_email(to_email, subject, body, from_email="your_email@gmail.com", password="your_app_password"):
    import smtplib
    from email.message import EmailMessage

    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(from_email, password)
    server.send_message(msg)
    server.quit()

def check_alerts():
    alerts = load_alerts()
    triggered = []

    for alert in alerts:
        symbol = alert["symbol"]
        alert_type = alert["alert_type"]
        target = alert["target_price"]
        contact_method = alert["contact_method"]
        contact = alert["contact"]

        ticker = yf.Ticker(symbol)
        price = ticker.info.get("regularMarketPrice")

        if price is None:
            print(f"[!] Couldn't get price for {symbol}")
            continue

        if alert_type == "Price goes ABOVE" and price >= target:
            triggered.append(alert)
            send_notification(alert, price)
        elif alert_type == "Price goes BELOW" and price <= target:
            triggered.append(alert)
            send_notification(alert, price)

    # Remove triggered alerts
    alerts = [a for a in alerts if a not in triggered]
    save_alerts(alerts)

def send_notification(alert, price):
    message = (
        f"📈 ALERT for {alert['symbol']}!\n"
        f"Condition met: {alert['alert_type']} ${alert['target_price']}\n"
        f"Current price: ${price:.2f}\n"
        f"AI Suggestion: Consider your position based on current momentum."
    )

    if alert["contact_method"] == "Email":
        send_email(alert["contact"], f"📢 Alert: {alert['symbol']}", message)
    else:
        print(f"[!] SMS not yet implemented — would send to {alert['contact']}")
        # You can plug in send_sms() here later

if __name__ == "__main__":
    check_alerts()
