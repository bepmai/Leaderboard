import requests

# URL API của SheetDB
SHEETDB_URL = "https://sheetdb.io/api/v1/ma8opp1ci2oqd"

# Gửi yêu cầu GET để lấy dữ liệu
response = requests.get(SHEETDB_URL)

# Kiểm tra trạng thái và in dữ liệu
if response.status_code == 200:
    data = response.json()
    print("Dữ liệu từ Google Sheets:")
    print(data)
else:
    print(f"Yêu cầu thất bại: {response.status_code}")