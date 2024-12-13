async function fetchAttendaceAmin() {
    try {
      const response = await fetch(`http://localhost:5000/api/attendance/attendance_admin`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json'
          },
          credentials:'include'
      });
  
      const data = await response.json();
  
      console.log("Dữ liệu nhận được:", data);

      populateTable(data['data']);

    } catch (error) {
      console.error("Lỗi khi gọi API:", error);
      document.getElementById("errorMessage").textContent = "Không thể tải dữ liệu.";
    }
  }

  function populateTable(data) {
    const tableBody = document.getElementById("AttendceTable"); // Lấy phần <tbody> của bảng

    // Xóa nội dung cũ trong bảng (nếu cần)
    tableBody.innerHTML = "";

    data.forEach((item, index) => {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${item['STT']}</td>
            <td>${item['Mã sinh viên']}</td>
            <td>${item['Họ']}</td>
            <td>${item['Tên']}</td>
            <td>${item['Lớp']}</td>
            <td>${item['1']}</td>
            <td>${item['2']}</td>
            <td>${item['3']}</td>
            <td>${item['4']}</td>
            <td>${item['5']}</td>
            <td>${item['6']}</td>
            <td>${item['7']}</td>
            <td>${item['8']}</td>
            <td>${item['9']}</td>
            <td>${item['10']}</td>
            <td>${item['11']}</td>
            <td>${item['12']}</td>
            <td>${item['13']}</td>
            <td>${item['14']}</td>
            <td>${item['15']}</td>
            <td>${item['Điểm project']}</td>
            <td>${item['Ghi chú']}</td>
            <td>${item['Vắng']}</td>
            <td>${item['Phát biểu']}</td>
        `;

        tableBody.appendChild(row);
    });
}

  document.addEventListener("DOMContentLoaded", fetchAttendaceAmin);
