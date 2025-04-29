import requests
import json
import os
import time

# 中央氣象署地震 API
CWB_API_URL = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/E-A0015-001?Authorization=CWA-6939BEE8-C910-4361-BC69-43F46EC3FD76"
WEBHOOK_URL = "https://hook.eu2.make.com/wa0099sdc5iorkyfaf8yqhv84iab98af"

# 儲存上一筆地震 ID 的檔案
EVENT_ID_FILE = "last_event_id.txt"

def load_last_event_id():
    if os.path.exists(EVENT_ID_FILE):
        with open(EVENT_ID_FILE, "r") as f:
            return f.read().strip()
    return ""

def save_last_event_id(event_id):
    with open(EVENT_ID_FILE, "w") as f:
        f.write(event_id)

def fetch_latest_earthquake():
    print("抓取地震資料中…")
    try:
        response = requests.get(CWB_API_URL)
        print("原始回應：", response.text[:200], "…")  # 只顯示前 200 字
        data = response.json()
        earthquakes = data["records"]["earthquake"]
        if not earthquakes:
            print("No earthquake data found")
            return None
        latest = earthquakes[0]
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
    try:
        res = requests.post(WEBHOOK_URL, json=payload)
        if res.status_code == 200:
            print("Webhook sent successfully.")
        else:
            print(f"Webhook failed. Status code: {res.status_code}. Retrying...")
            retry = requests.post(WEBHOOK_URL, json=payload)
            print("Retry status:", retry.status_code)
    except Exception as e:
        print("Webhook error:", e)

def main():
    last_event_id = load_last_event_id()
    latest_eq = fetch_latest_earthquake()

    if latest_eq is None:
        print("No new earthquake detected.")
        return

    current_event_id = latest_eq["earthquakeNo"]
    print("上次地震編號:", last_event_id)
    print("本次地震編號:", current_event_id)

    if current_event_id != last_event_id:
        print("新地震偵測到！")
        send_to_webhook(latest_eq)
        save_last_event_id(current_event_id)
    else:
        print("No new earthquake detected.")

if __name__ == "__main__":
    main()