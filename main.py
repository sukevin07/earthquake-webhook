import requests
import json
import os
import time

CWB_API_URL = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/E-A0015-001"
API_KEY = "CWA-6939BEE8-C910-4361-BC69-43F46EC3FD76"
WEBHOOK_URL = "https://hook.eu2.make.com/wa0099sdc5iorkyfaf8yqhv84iab98af"

def load_last_event_id():
    if os.path.exists("last_event_id.txt"):
        with open("last_event_id.txt", "r") as f:
            return f.read().strip()
    return ""

def save_last_event_id(event_id):
    with open("last_event_id.txt", "w") as f:
        f.write(event_id)

def fetch_latest_earthquake():
    try:
        headers = {"Authorization": API_KEY}
        print("抓取地震資料中...")
        res = requests.get(CWB_API_URL, headers=headers, timeout=10)
        print("資料成功取得")
        data = res.json()
        records = data["records"]["earthquake"]
        if not records:
            return None
        latest = records[0]
        return latest
    except Exception as e:
        print("Error fetching data:", e)
        return None

def send_to_webhook(earthquake):
    info = earthquake["earthquakeInfo"]
    report_time = earthquake["reportContent"]
    payload = {
        "location": info["epicenter"]["location"],
        "magnitude": info["magnitude"]["value"],
        "depth": info["depth"]["value"],
        "time": info["originTime"],
        "report": report_time
    }
    res = requests.post(WEBHOOK_URL, json=payload)
    print("Webhook sent:", res.status_code, res.text)

def main_loop():
    while True:
        last_event_id = load_last_event_id()
        latest_eq = fetch_latest_earthquake()
        if latest_eq is None:
            print("No earthquake detected.")
        else:
            event_id = latest_eq["earthquakeNo"]
            if event_id != last_event_id:
                print("New earthquake detected:", event_id)
                send_to_webhook(latest_eq)
                save_last_event_id(event_id)
            else:
                print("No new earthquake detected.")
        print("等待 30 秒...")
        time.sleep(30)

if __name__ == "__main__":
    main_loop()