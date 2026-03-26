import json
import os
import requests
import re
from datetime import datetime
from zoneinfo import ZoneInfo

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

API_URL = "https://cdn.funder.co.il/funder/wsStock.asmx/GetindicesOn"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": text})

def get_chart_api_id(fund_id):
    try:
        url = f"https://www.funder.co.il/fund/{fund_id}"
        res = requests.get(url, headers=HEADERS, timeout=10)
        
        # מחפש chartApiId
        match = re.search(r'chartApiId["\']?\s*value=["\'](\d+)', res.text)
        
        if match:
            return match.group(1)

        # fallback
        match2 = re.search(r'chartApiId.*?(\d+)', res.text)
        if match2:
            return match2.group(1)

        return None

    except:
        return None

def fetch_fund_data(chart_id):
    try:
        params = {"idx": chart_id}

        res = requests.get(API_URL, params=params, headers=HEADERS, timeout=10)
        data = res.json()

        return str(data)[:80]

    except Exception as e:
        return f"שגיאה: {str(e)[:30]}"

def build_report(funds):
    now_il = datetime.now(ZoneInfo("Asia/Jerusalem")).strftime("%d/%m/%Y %H:%M")

    lines = [f"סיכום יומי - {now_il}", ""]

    for fund_id in funds:
        chart_id = get_chart_api_id(fund_id)

        if not chart_id:
            lines.append(f"{fund_id}")
            lines.append("לא נמצא chartApiId")
            lines.append("")
            continue

        data = fetch_fund_data(chart_id)

        lines.append(f"{fund_id}")
        lines.append(f"chartApiId: {chart_id}")
        lines.append(f"DATA: {data}")
        lines.append("")

    return "\n".join(lines)

if __name__ == "__main__":
    with open("stocks.json", "r") as f:
        funds = json.load(f)

    report = build_report(funds)
    send_telegram_message(report)
