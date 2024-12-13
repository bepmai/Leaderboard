async function fetchAttendaceUsers() {
    try {
      const msv = getCookie('msv');
  
      if (!msv) {
          console.error("Token không tồn tại trong cookie!");
          return;
      }
      const response = await fetch(`http://localhost:5000/api/attendance/attendance_users?id=${msv}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json'
          },
          credentials:'include'
      });
  
      const data = await response.json();
  
      console.log("Dữ liệu nhận được:", data);

      const tableBody = document.getElementById("AttendceTable"); // Lấy phần <tbody> của bảng

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

  // fetchAttendaceUsers();
