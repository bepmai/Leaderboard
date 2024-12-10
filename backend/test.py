import requests

# URL API của SheetDB
SHEETDB_URL = "https://sheetdb.io/api/v1/ma8opp1ci2oqd"

# Gửi yêu cầu GET để lấy dữ liệu
response = requests.get(SHEETDB_URL)

# Kiểm tra trạng thái và in dữ liệu
if response.status_code == 200:
    data = response.json()  # Lấy dữ liệu JSON từ SheetDB
    # Lọc bản ghi có Mã sinh viên là 2151163664
    student_data = [record for record in data if record.get("Mã sinh viên") == "2151163664"]
    
    if student_data:
        print("Bản ghi tìm thấy:")
        print(student_data)
    else:
        print("Không tìm thấy bản ghi với Mã sinh viên là 2151163664.")
else:
    print(f"Yêu cầu thất bại: {response.status_code}")
