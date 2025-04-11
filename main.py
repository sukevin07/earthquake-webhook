import requests

print("抓取地震資料中...")
try:
    # 使用你提供的 API 金鑰
    response = requests.get("https://opendata.cwa.gov.tw/api/v1/rest/datastore/E-A0015-001?Authorization=CWA-6939BEE8-C910-4361-BC69-43F46EC3FD76")
    response.raise_for_status()
    data = response.json()  # 正確方式，不需要再 json.loads()
    print("資料成功取得")

    # 測試 webhook 呼叫
    webhook_url = 'https://hook.eu2.make.com/wa0099sdc5iorkyfaf8yqhv84iab98af'
    payload = {"message": "這是從 GitHub Actions 發出的測試訊息"}
    r = requests.post(webhook_url, json=payload)
    print(f"Webhook 回傳狀態碼: {r.status_code}")

except Exception as e:
    print(f"Error fetching data: {e}")
