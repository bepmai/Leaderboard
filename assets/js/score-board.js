async function fetchSoreBoardAdmin() {
    try {
      const response = await fetch(`http://localhost:5000/api/score_board/score_board_admin`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json'
          },
          credentials:'include'
      });
  
      const data = await response.json();
  
      console.log("Dữ liệu nhận được:", data);

      const tableBody = document.getElementById("SoreBoardTable"); // Lấy phần <tbody> của bảng

        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${data['data'][0]['STT']}</td>
            <td>${data['data'][0]['Mã sinh viên']}</td>
            <td>${data['data'][0]['Họ ']} ${data['data'][0]['Tên']}</td>
            <td>${data['data'][0]['Lớp']}</td>
            <td>${data['data'][0]['Lên bảng']}</td>
            <td>${data['data'][0]['Mindmap tổng hợp']}</td>
            <td>${data['data'][0]['Code hệ thống']}</td>
            <td>${data['data'][0]['Tổng điểm tích cực']}</td>
        `;

        tableBody.appendChild(row);

    } catch (error) {
      console.error("Lỗi khi gọi API:", error);
      document.getElementById("errorMessage").textContent = "Không thể tải dữ liệu.";
    }
  }
  document.addEventListener("DOMContentLoaded", fetchSoreBoardAdmin);