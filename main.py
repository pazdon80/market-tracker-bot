import json
import os
import requests
from datetime import datetime
from zoneinfo import ZoneInfo
from bs4 import BeautifulSoup

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

BASE_URL = "https://www.funder.co.il/fund/"

def send_telegram_message(text: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text
    }
    requests.post(url, json=payload)

def fetch_fund_data(fund_id):
    try:
        url = BASE_URL + fund_id
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        title = soup.find("title").text.strip()

        # ניסיון למצוא שינוי יומי
        change = "לא נמצא"
        for span in soup.find_all("span"):
            if "%" in span.text:
                change = span.text.strip()
                break

        # כתבות (כותרות בלבד בשלב ראשון)
        articles = []
        for a in soup.find_all("a"):
            if "article" in a.get("href", ""):
                articles.append(a.text.strip())

        articles = list(set(articles))[:3]

        return {
            "title": title,
            "change": change,
            "articles": articles
        }

    except Exception as e:
        return {
            "title": fund_id,
            "change": "שגיאה",
            "articles": []
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

        lines.append(f"{data['title']}")
        lines.append(f"שינוי יומי: {data['change']}")
        lines.append(f"חריג: {anomaly}")

        if data["articles"]:
            lines.append("סיכום כתבות:")
            for art in data["articles"]:
                lines.append(f"- {art[:80]}")
        else:
            lines.append("סיכום כתבות: אין עדכונים")

        lines.append("")

    return "\n".join(lines)

if __name__ == "__main__":
    with open("stocks.json", "r") as f:
        funds = json.load(f)

    report = build_report(funds)
    send_telegram_message(report)
