import requests

# URL API của SheetDB
SHEETDB_URL = "https://sheetdb.io/api/v1/i1u4fa5bv8sk5"

# Gửi yêu cầu GET để lấy dữ liệu
response = requests.get(SHEETDB_URL)

# Kiểm tra trạng thái và in dữ liệu
if response.status_code == 200:
    data = response.json()
    print("Dữ liệu từ Google Sheets:")
    print(data)
else:
    print(f"Yêu cầu thất bại: {response.status_code}")