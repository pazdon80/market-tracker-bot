import requests
from urllib.parse import urlencode

CANDIDATE_URLS = [
    "https://www.funder.co.il/wsStock.asmx/GetindicesOn",
    "https://www.funder.co.il/funder/wsStock.asmx/GetindicesOn",
    "https://cdn.funder.co.il/funder/wsStock.asmx/GetindicesOn",
]

def test_url(fund_id: str) -> None:
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": f"https://www.funder.co.il/fund/{fund_id}",
    }

    params_options = [
        {"idx": fund_id},
        {"idx": fund_id, "callback": "jQuery123"},
        {"idx": fund_id, "jsoncallback": "jQuery123"},
    ]

    for url in CANDIDATE_URLS:
        for params in params_options:
            try:
                response = requests.get(
                    url,
                    params=params,
                    headers=headers,
                    timeout=20,
                )

                body_preview = response.text[:500].replace("\n", " ").replace("\r", " ")

                print("\n" + "=" * 90)
                print("URL:", response.url)
                print("STATUS:", response.status_code)
                print("CONTENT-TYPE:", response.headers.get("Content-Type"))
                print("BODY:", body_preview)

            except Exception as e:
                print("\n" + "=" * 90)
                print("URL:", url, params)
                print("ERROR:", e)

if __name__ == "__main__":
    test_url("5139332")
