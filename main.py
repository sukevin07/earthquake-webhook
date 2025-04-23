import requests
import json
import os

API_KEY = "CWA-6939BEE8-C910-4361-BC69-43F46EC3FD76"
WEBHOOK_URL = "https://hook.eu2.make.com/wa0099sdc5iorkyfaf8yqhv84iab98af"
CWB_API_URL = f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/E-A0015-001?Authorization={API_KEY}"

def load_last_event_id():
    if os.path.exists("last_event_id.txt"):
        with open("last_event_id.txt", "r") as f:
            return f.read().strip()
    return ""

def save_last_event_id(event_id):
    with open("last_event_id.txt", "w") as f:
        f.write(event_id)

def fetch_latest_earthquake():
    print("抓取地震資料中…")
    try:
        res = requests.get(CWB_API_URL)
        data = res.json()
        if "records" not in data or "earthquake" not in data["records"]:
            print("No earthquake data found")
            return None
        records = data["records"]["earthquake"]
        if not records:
            print("No recent earthquakes")
            return None
        print("資料成功取得")
        return records[0]
    except Exception as e:
        print("Error fetching data:", e)
        return None

def send_to_webhook(earthquake):
    info = earthquake["earthquakeInfo"]
    payload = {
        "location": info["epicenter"]["location"],
        "magnitude": info["magnitude"]["value"],
        "depth": info["depth"]["value"],
        "time": info["originTime"],
        "report": earthquake["reportContent"]
    }
    try:
        res = requests.post(WEBHOOK_URL, json=payload)
        print("Webhook sent:", res.status_code)
    except Exception as e:
        print("Webhook Error:", e)

def main():
    last_event_id = load_last_event_id()
    latest_eq = fetch_latest_earthquake()
    if latest_eq is None:
        print("No new earthquake detected.")
        return
    event_id = latest_eq["earthquakeNo"]
    if event_id != last_event_id:
        print("New earthquake detected:", event_id)
        send_to_webhook(latest_eq)
        save_last_event_id(event_id)
    else:
        print("No new earthquake.")

if __name__ == "__main__":
    main()