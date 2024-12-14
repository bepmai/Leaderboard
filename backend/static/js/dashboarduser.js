if (getCookie('token') == null) {
  window.location.href = "/"
}
const msv = getCookie('msv');
async function fetchDashboardUsersInfo() {
  try {
    if (!msv) {
      console.error("Token không tồn tại trong cookie!");
      return;
    }
    const response = await fetch(`${domain}/api/dashboard/dashboard_info_users?id=${msv}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      },
      credentials: 'include'
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data = await response.json();

    document.getElementById("number_of_school_attendance").textContent = data.number_of_school_attendance + " người" || "N/A";
    document.getElementById("number_of_break").textContent = data.number_of_break + " người" || "N/A";
    document.getElementById("Number_of_speeches_cluster").textContent = data.Number_of_speeches_cluster + " lần" || "N/A";
    document.getElementById("rank").textContent = "Thứ " + data.rank || "N/A";

    console.log("Dữ liệu nhận được:", data);
  } catch (error) {
    console.error("Lỗi khi gọi API:", error);
    document.getElementById("errorMessage").textContent = "Không thể tải dữ liệu.";
  }
}

document.addEventListener("DOMContentLoaded", fetchDashboardUsersInfo);

const pieData = {
  labels: ["Đi học", "Nghỉ học"],
  datasets: [
    {
      data: [85, 15], // Tỷ lệ %
      backgroundColor: ["#3498db", "#e74c3c"], // Màu sắc
    },
  ],
};

// Pie chart configuration
const pieConfig = {
  type: "pie",
  data: pieData,
  options: {
    responsive: false,
    maintainAspectRatio: false,
    plugins: {
      tooltip: {
        callbacks: {
          label: function (context) {
            const label = context.label || "";
            const value = context.raw || 0;
            const total = context.dataset.data.reduce(
              (sum, val) => sum + val,
              0
            );
            const percentage = ((value / total) * 100).toFixed(2);
            return `${label}: ${percentage}%`;
          },
        },
      },
      datalabels: {
        color: "#fff", // Màu chữ
        font: {
          size: 16,
          weight: "bold",
        },
        formatter: (value, context) => {
          const total = context.chart.data.datasets[0].data.reduce(
            (sum, val) => sum + val,
            0
          );
          const percentage = ((value / total) * 100).toFixed(2);
          return `${percentage}%`; // Hiển thị % trên biểu đồ
        },
      },
    },
  },
  plugins: [ChartDataLabels], // Kích hoạt plugin
};

// Render pie chart
const pieChart = document.getElementById("pieChart").getContext("2d");
const chartInstance = new Chart(pieChart, pieConfig);
const lineData = {
  labels: ["11/11", "15/11", "19/11", "22/11", "26/11", "29/11", "3/12", "6/12", "10/12", "0/12", "0/12", "0/12", "0/12", "0/12", "0/12"], // Ngày
  datasets: [
    {
      label: "Trạng thái",
      data: [0, 1, 1, 0, 1], // 0: Nghỉ học, 1: Đi học
      borderColor: "#3498db",
      backgroundColor: "#3498db",
      pointBackgroundColor: "#3498db",
      borderWidth: 2,
      fill: false, // Không tô màu phía dưới đường
    },
  ],
};

// Cấu hình biểu đồ
const lineConfig = {
  type: "line", // Có thể đổi thành "bar" nếu muốn sử dụng biểu đồ cột
  data: lineData,
  options: {
    responsive: true,
    plugins: {
      legend: {
        display: false, // Ẩn chú thích (nếu không cần thiết)
      },
    },
    scales: {
      x: {
        title: {
          display: true,
          text: "Ngày", // Tiêu đề trục X
        },
      },
      y: {
        ticks: {
          stepSize: 1, // Giá trị tăng theo bước 1
          callback: function (value) {
            return value === 1 ? "Đi học" : "Nghỉ học"; // Hiển thị trạng thái thay vì số
          },
        },
        min: 0,
        max: 1,
      },
    },
  },
};

// Render biểu đồ - phat bieu
const ctx = document.getElementById("lineChart").getContext("2d");
lineChartInstance = new Chart(ctx, lineConfig);
const ctxParticipation = document
  .getElementById("chartParticipation")
  .getContext("2d");
charClusterState = new Chart(ctxParticipation, {
  type: "line",
  data: {
    labels: ["Lên bảng", "Mindmap tổng hợp", "Code hệ thống"],
    datasets: [
      {
        label: "Số lần phát biểu",
        data: [3, 1, 1],
        borderColor: "#3498db",
        borderWidth: 2,
        fill: false,
        pointBackgroundColor: "#3498db",
        tension: 0.3,
      },
    ],
  },
  options: {
    responsive: false,
    maintainAspectRatio: false,
  },
});
const pieGetData = async () => {
  try {
    const response = await fetch(`${domain}/api/dashboard/chart/absent_msv/${msv}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      },
      credentials: 'include'
    });

    const absentData = await response.json();
    const absentPercent = absentData.data / (15 / 100);
    const attendancePercent = (15 - absentData.data) / (15 / 100);
    // Làm tròn giá trị
    const roundedAbsentPercent = Math.round(absentPercent * 100) / 100;
    const roundedAttendancePercent = Math.round(attendancePercent * 100) / 100;

    // Cập nhật dữ liệu
    const data = [roundedAttendancePercent, roundedAbsentPercent];
    pieConfig.data.datasets[0].data = data;

    if (chartInstance) {
      chartInstance.update();
    }
  } catch (error) {
    console.log(error);
  }
};

const lineGetData = async () => {
  try {
    const listatten = [];
    const requests = [];
    for (let i = 1; i <= 15; i++) {
      const request = await fetch(`${domain}/api/dashboard/chart/absent_msv/${msv}/${i}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        },
        credentials: 'include'
      });
      requests.push(request);
    }
    const responses = await Promise.all(requests);
    const dataList = await Promise.all(responses.map(response => response.json()));
    for (let i = 0; i < dataList.length; i++) {
      listatten.push(dataList[i].data[1])
    }
    lineData.datasets[0].data = listatten;
    if (lineChartInstance) {
      lineChartInstance.update();
    }
  }
  catch (error) {
    console.log(error)
  }
}
const clusterGetData = async () => {
  try {
    const request = await fetch(`${domain}/api/dashboard/chart/stated/group/${msv}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      },
      credentials: 'include'
    });
    const responses = await request.json();
    console.log(responses)
    const list= [responses.data[0],responses.data[1],responses.data[2]]
    charClusterState.data.datasets[0].data = list;
    if (charClusterState) {
      charClusterState.update()
    }
  }
  catch (error) {
    console.log(error)
  }
}
pieGetData()
lineGetData()
clusterGetData()