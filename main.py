import json
import os
import requests

CANDIDATE_URLS = [
    "https://www.funder.co.il/wsStock.asmx/GetindicesOn",
    "https://www.funder.co.il/funder/wsStock.asmx/GetindicesOn",
    "https://cdn.funder.co.il/funder/wsStock.asmx/GetindicesOn",
]

def test_url(fund_id: str):
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": f"https://www.funder.co.il/fund/{fund_id}",
    }

    for url in CANDIDATE_URLS:
        try:
            res = requests.post(
                url,
                data={"idx": fund_id},
                headers=headers,
                timeout=15,
            )
            text = res.text[:500].replace("\n", " ").replace("\r", " ")
            print("=" * 80)
            print("URL:", url)
            print("STATUS:", res.status_code)
            print("CONTENT-TYPE:", res.headers.get("Content-Type"))
            print("BODY:", text)
        except Exception as e:
            print("=" * 80)
            print("URL:", url)
            print("ERROR:", str(e))

if __name__ == "__main__":
    test_url("5139332")
