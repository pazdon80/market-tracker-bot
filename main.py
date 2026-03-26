import json
import os
import requests
from datetime import datetime

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    raise ValueError("Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID environment variables")

with open("stocks.json", "r", encoding="utf-8") as f:
    instruments = json.load(f)

def send_telegram_message(text: str) -> None:
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text
    }
    response = requests.post(url, json=payload, timeout=30)
    response.raise_for_status()

def build_report() -> str:
    today = datetime.now().strftime("%d/%m/%Y %H:%M")

    lines = [
        f"סיכום יומי - {today}",
        "",
        "רשימת הניירות למעקב:",
    ]

    for instrument in instruments:
        lines.append(f"- {instrument}")

    lines += [
        "",
        "זה שלב ראשון של המערכת.",
        "בשלב הבא נחבר נתוני שוק, סיווג ישראל/חו״ל, סוג נכס, שינוי יומי, שער עדכני, כתבות וחריגות."
    ]

    return "\n".join(lines)

if __name__ == "__main__":
    report = build_report()
    send_telegram_message(report)
    print("Message sent successfully.")
