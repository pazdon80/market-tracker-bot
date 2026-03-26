import json
import os
import requests
from datetime import datetime
from zoneinfo import ZoneInfo

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

API_URL = "https://www.funder.co.il/wsStock.asmx/GetindicesOn"

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
    requests.post(url, json=payload)

def fetch_fund_data(fund_id):
    try:
        payload = {"idx": fund_id}

        res = requests.post(API_URL, data=payload, timeout=10)
        text = res.text.strip()

        # ניקוי JSONP
        if text.startswith("("):
            text = text[1:-1]

        return {
            "change": text[:50],  # רק כדי לראות מה חוזר
            "price": "-"
        }

    except Exception as e:
        return {
            "change": f"שגיאה: {str(e)[:20]}",
            "price": "-"
        }

    except Exception as e:
        return {
            "change": "שגיאה",
            "price": "-"
        }

def detect_anomaly(change_text):
    try:
        change = float(change_text.replace("%", "").replace("+", "").replace(",", "."))
        return abs(change) > 1
    except:
        return False

def build_report(funds):
    now_il = datetime.now(ZoneInfo("Asia/Jerusalem")).strftime("%d/%m/%Y %H:%M")

    lines = [f"סיכום יומי - {now_il}", ""]

    for fund_id in funds:
        data = fetch_fund_data(fund_id)

        anomaly = "כן 🚨" if detect_anomaly(data["change"]) else "לא"

        lines.append(f"{fund_id}")
        lines.append(f"שינוי יומי: {data['change']}")
        lines.append(f"חריג: {anomaly}")
        lines.append("")

    return "\n".join(lines)

if __name__ == "__main__":
    with open("stocks.json", "r") as f:
        funds = json.load(f)

    report = build_report(funds)
    send_telegram_message(report)
