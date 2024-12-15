if(getCookie('token')==null){
  window.location.href="/"
}
const msv = getCookie('msv');
const socket = io();

function joinRoom() {
  if (msv) {
    socket.emit('join', { 'msv': msv });
  }
}

joinRoom();

socket.on('receive_data', function(data) {
  fetchAttendaceUsers();
  fetchSoreBoardUsers();
});

async function fetchAttendaceUsers() {
    try {
      if (!msv) {
          console.error("Token không tồn tại trong cookie!");
          return;
      }
      const response = await fetch(`${domain}/api/attendance/attendance_users?id=${msv}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json'
          },
          credentials:'include'
      });
  
      const data = await response.json();
  
      console.log("Dữ liệu nhận được:", data);

      const tableBody = document.getElementById("AttendceTable"); // Lấy phần <tbody> của bảng

      tableBody.innerHTML = "";

        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${data['data'][0]['STT']}</td>
            <td>${data['data'][0]['Mã sinh viên']}</td>
            <td>${data['data'][0]['Họ']}</td>
            <td>${data['data'][0]['Tên']}</td>
            <td>${data['data'][0]['Lớp']}</td>
            <td>${data['data'][0]['1']}</td>
            <td>${data['data'][0]['2']}</td>
            <td>${data['data'][0]['3']}</td>
            <td>${data['data'][0]['4']}</td>
            <td>${data['data'][0]['5']}</td>
            <td>${data['data'][0]['6']}</td>
            <td>${data['data'][0]['7']}</td>
            <td>${data['data'][0]['8']}</td>
            <td>${data['data'][0]['9']}</td>
            <td>${data['data'][0]['10']}</td>
            <td>${data['data'][0]['11']}</td>
            <td>${data['data'][0]['12']}</td>
            <td>${data['data'][0]['13']}</td>
            <td>${data['data'][0]['14']}</td>
            <td>${data['data'][0]['15']}</td>
            <td>${data['data'][0]['Điểm project']}</td>
            <td>${data['data'][0]['Ghi chú']}</td>
            <td>${data['data'][0]['Vắng']}</td>
            <td>${data['data'][0]['Phát biểu']}</td>
        `;

        tableBody.appendChild(row);

    } catch (error) {
      console.error("Lỗi khi gọi API:", error);
      document.getElementById("errorMessage").textContent = "Không thể tải dữ liệu.";
    }
  }

async function fetchSoreBoardUsers() {
    try {
      const msv = getCookie('msv');
  
      if (!msv) {
          console.error("Token không tồn tại trong cookie!");
          return;
      }
      const response = await fetch(`${domain}/api/score_board/score_board_users?id=${msv}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json'
          },
          credentials:'include'
      });
  
      const data = await response.json();
  
      console.log("Dữ liệu nhận được:", data);

      const tableBody = document.getElementById("SoreBoardTable"); // Lấy phần <tbody> của bảng

      tableBody.innerHTML = "";

        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${data['data'][0]['STT']}</td>
            <td>${data['data'][0]['Mã sinh viên']}</td>
            <td>${data['data'][0]['Họ ']}</td>
            <td>${data['data'][0]['Tên']}</td>
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
  document.addEventListener("DOMContentLoaded", fetchAttendaceUsers);
  document.addEventListener("DOMContentLoaded", fetchSoreBoardUsers);
