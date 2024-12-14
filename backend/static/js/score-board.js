const msv = getCookie('msv');
const socket = io();

function joinRoom() {
  if (msv) {
    socket.emit('join', { 'msv': msv });
  }
}

joinRoom();

socket.on('receive_data', function(data) {
  fetchSoreBoardAdmin();
});

async function fetchSoreBoardAdmin() {
    try {
      const response = await fetch(`${domain}/api/score_board/score_board_admin`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json'
          },
          credentials:'include'
      });
  
      const data = await response.json();
  
      console.log("Dữ liệu nhận được:", data);

      populateTable(data['data'])

    } catch (error) {
      console.error("Lỗi khi gọi API:", error);
      document.getElementById("errorMessage").textContent = "Không thể tải dữ liệu.";
    }
  }
  function populateTable(data) {
    const tableBody = document.getElementById("SoreBoardTable"); // Lấy phần <tbody> của bảng

    // Xóa nội dung cũ trong bảng (nếu cần)
    tableBody.innerHTML = "";

    data.forEach((item, index) => {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${item['STT']}</td>
            <td>${item['Mã sinh viên']}</td>
            <td>${item['Họ ']}</td>
            <td>${item['Tên']}</td>
            <td>${item['Lớp']}</td>
            <td>${item['Lên bảng']}</td>
            <td>${item['Mindmap tổng hợp']}</td>
            <td>${item['Code hệ thống']}</td>
            <td>${item['Tổng điểm tích cực']}</td>
        `;

        tableBody.appendChild(row);
    });
}
  document.addEventListener("DOMContentLoaded", fetchSoreBoardAdmin);