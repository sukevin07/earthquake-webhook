import requests

# 檢查地震事件是否已經發送過
def is_earthquake_sent(event_id):
    try:
        with open("sent_earthquakes.txt", "r") as file:
            sent_ids = file.read().splitlines()
        return event_id in sent_ids
    except FileNotFoundError:
        return False

# 標記已發送的地震事件
def mark_earthquake_as_sent(event_id):
    with open("sent_earthquakes.txt", "a") as file:
        file.write(f"{event_id}\n")

print("抓取地震資料中...")
try:
    # 使用中央氣象署的 API 取得地震資料
    response = requests.get("https://opendata.cwa.gov.tw/api/v1/rest/datastore/E-A0015-001?Authorization=CWA-6939BEE8-C910-4361-BC69-43F46EC3FD76")
    response.raise_for_status()
    data = response.json()  # 正確方式，將回傳的 JSON 解析

    print("資料成功取得")

    # 假設抓取第一筆地震資料
    earthquake = data['records']['earthquake'][0]
    event_id = earthquake['earthquake_id']  # 每個地震事件都有唯一的 ID
    magnitude = earthquake['magnitude']
    latitude = earthquake['latitude']
    longitude = earthquake['longitude']
    location = earthquake['location']

    # 檢查這筆地震事件是否已經發送過
    if is_earthquake_sent(event_id):
        print("此地震事件已經發送過，跳過此次發送。")
    else:
        # 根據地震資料生成訊息
        message = f"地震發生！\n震中位置：{location}\n震中經緯度：({latitude}, {longitude})\n震級：{magnitude}"

        # 測試 webhook 呼叫
        webhook_url = 'https://hook.eu2.make.com/wa0099sdc5iorkyfaf8yqhv84iab98af'  # 你的 Webhook URL
        payload = {"message": message}
        r = requests.post(webhook_url, json=payload)

        # 如果發送成功，標記這筆地震事件已發送
        if r.status_code == 200:
            mark_earthquake_as_sent(event_id)

        print(f"Webhook 回傳狀態碼: {r.status_code}")

except Exception as e:
    print(f"Error fetching data: {e}")
