if (getCookie('token') == null) {
  window.location.href = "/"
}
if(getCookie('role')!="admin"){
  window.location.href="dashboarduser"
}
var allsv;
const msv = getCookie('msv');
async function fetchDashboardInfo() {
  try {
    const token = getCookie("token");

    if (!token) {
      console.error("Token không tồn tại trong cookie!");
      return;
    }
    const response = await fetch(`${domain}/api/dashboard/dashboard_info_admin`, {
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

    document.getElementById("School_attendance_rate").textContent = data.School_attendance_rate + " người" || "N/A";
    document.getElementById("Break_rate").textContent = data.Break_rate + " người" || "N/A";
    document.getElementById("number_of_speeches").textContent = data.number_of_speeches + " lần" || "N/A";

    console.log("Dữ liệu nhận được:", data);
  } catch (error) {
    console.error("Lỗi khi gọi API:", error);
    document.getElementById("errorMessage").textContent = "Không thể tải dữ liệu.";
  }
}

document.addEventListener("DOMContentLoaded", fetchDashboardInfo);

function checkLoginStatus() {
  const msv = getCookie('msv');
  if (!msv) {
    window.location.href = "sign-in.html"
  }
}

window.onload = checkLoginStatus;


const ctxAbsences = document.getElementById('chartAbsences');
new Chart(ctxAbsences, {
  type: 'line',
  data: {
    labels: ['Tuần 1', 'Tuần 2', 'Tuần 3', 'Tuần 4'],
    datasets: [{
      label: 'Số buổi nghỉ',
      data: [1, 2, 1, 1],
      backgroundColor: '#e74c3c',
      fill: false,
      tension: 0.3
    }]
  },
  options: {
    responsive: true
  }
});
const pieData = {
  labels: ["Đi học", "Nghỉ học"],
  datasets: [
    {
      data: [80, 20], // Tỷ lệ % ban đầu
      backgroundColor: ["#3498db", "#e74c3c"], // Màu sắc
    },
  ],
};

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
            const total = context.dataset.data.reduce((sum, val) => sum + val, 0);
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
          const total = context.chart.data.datasets[0].data.reduce((sum, val) => sum + val, 0);
          const percentage = ((value / total) * 100).toFixed(2);
          return `${percentage}%`; // Hiển thị % trên biểu đồ
        },
      },
    },
  },
  plugins: [ChartDataLabels], // Kích hoạt plugin
};

const pieGetData = async () => {
  try {
    const response = await fetch(`${domain}/api/dashboard/chart/absent`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      },
      credentials: 'include'
    });

    const absentData = await response.json();
    const absentPercent = absentData.data[0] / (absentData.data[1] * 15 / 100);
    const attendancePercent = (15 * absentData.data[1] - absentData.data[0]) / (absentData.data[1] * 15 / 100);

    allsv = absentData.data[1]
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

// Tạo biểu đồ khi trang được tải
const ctx = document.getElementById("pieChart").getContext("2d");
const chartInstance = new Chart(ctx, pieConfig);



// Render pie chart


const lineData = {
  labels: ["11/11", "15/11", "19/11", "22/11", "26/11", "29/11", "3/12", "6/12", "10/12", "0/12", "0/12", "0/12", "0/12", "0/12", "0/12"], // Ngày
  datasets: [
    {
      label: "Số sinh viên đi học",
      data: [30, 28, 32, 35, 30, 30, 28, 32, 35, 30, 30, 28, 32, 35, 30], // Số lượng
      borderColor: "#3498db",
      backgroundColor: "rgba(52, 152, 219, 0.2)",
      fill: true,
    },
    {
      label: "Số sinh viên nghỉ học",
      data: [5, 7, 3, 2, 4, 5, 7, 3, 2, 4, 5, 7, 3, 2, 4], // Số lượng
      borderColor: "#e74c3c",
      backgroundColor: "rgba(231, 76, 60, 0.2)",
      fill: true,
    },
  ],
};

// Line chart configuration
const lineConfig = {
  type: "line",
  data: lineData,
  options: {
    scales: {
      x: {
        title: {
          display: true,
          text: "Ngày",
        },
      },
      y: {
        title: {
          display: true,
          text: "Số sinh viên",
        },
      },
    },
  },
};

// Render line chart
const lineChartInstance = new Chart(document.getElementById("lineChart"), lineConfig);

const lineGetData = async () => {
  try {
    const listadsent = [];
    const listatten = [];
    const requests = [];
    for (let i = 1; i <= 15; i++) {
      const request = await fetch(`${domain}/api/dashboard/chart/absent/${i}`, {
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
      listadsent.push(dataList[i].data[0])
      listatten.push(dataList[i].data[1])
    }
    lineData.datasets[0].data = listatten;
    lineData.datasets[1].data = listadsent;
    if (lineChartInstance) {
      lineChartInstance.update();
    }
  }
  catch (error) {
    console.log(error)
  }
}
// Biểu đồ đường: Số lần phát biểu lớp
const ctxParticipation = document.getElementById('chartParticipation').getContext('2d');
const chartParticipationInstance = new Chart(ctxParticipation, {
  type: 'line',
  data: {
    labels: ["11/11", "15/11", "19/11", "22/11", "26/11", "29/11", "3/12", "6/12", "10/12", "0/12", "0/12", "0/12", "0/12", "0/12", "0/12"], // Ngày
    datasets: [
      {
        label: 'Số lần phát biểu',
        data: [0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        borderColor: '#3498db',
        borderWidth: 2,
        fill: false,
        pointBackgroundColor: '#3498db',
        tension: 0.3,
      },
    ],
  },
  options: {
    responsive: true, // Tự động thay đổi kích thước
    plugins: {
      legend: {
        display: true, // Hiển thị chú thích
        position: 'top',
      },
      tooltip: {
        callbacks: {
          label: function (tooltipItem) {
            return `Số lần phát biểu: ${tooltipItem.raw}`;
          },
        },
      },
    },
    scales: {
      x: {
        title: {
          display: true,
          text: 'Ngày', // Tiêu đề trục X
          font: {
            size: 14,
          },
        },
        ticks: {
          stepSize: 1, // Bước nhảy trên trục X
          beginAtZero: true,
        },
      },
      y: {
        title: {
          display: true,
          text: 'Số lần phát biểu', // Tiêu đề trục Y
          font: {
            size: 14,
          },
        },
        ticks: {
          stepSize: 1, // Bước nhảy trên trục Y
          beginAtZero: true,
        },
      },
    },
  },
});
const partyGetData = async () => {
  try {
    const liststated = [];
    const requests = [];
    for (let i = 1; i <= 15; i++) {
      const request = await fetch(`${domain}/api/dashboard/chart/stated/${i}`, {
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
      liststated.push(dataList[i].data[0])
    }
    chartParticipationInstance.data.datasets[0].data = liststated;
    if (chartParticipationInstance) {
      chartParticipationInstance.update();
    }
  }
  catch (error) {
    console.log(error)
  }
}

// Biểu đồ đường: Số lần phát biểu -cụm
const ctxParticipationCluster = document
  .getElementById('chartParticipationCluster')
  .getContext('2d');
const charClusterState = new Chart(ctxParticipationCluster, {
  type: 'line',
  data: {
    labels: ['Đức Anh', 'Bách', 'Đạo', 'Dũng', 'Giang', 'Hậu', 'Hiếu', 'Hùng', 'Hường', 'Lê', 'Mai'],
    datasets: [
      {
        label: 'Số lần phát biểu',
        data: [3, 3, 3, 5, 2, 5, 0, 0, 1, 1, 5],
        borderColor: '#3498db',
        borderWidth: 2,
        fill: false,
        pointBackgroundColor: '#3498db',
        tension: 0.3,
      },
    ],
  },
  options: {
    responsive: true,
    scales: {
      x: {
        title: {
          display: true,
          text: 'Tên thành viên',
          font: {
            size: 14,
          },
        },
      },
      y: {
        title: {
          display: true,
          text: 'Số lần phát biểu',
          font: {
            size: 14,
          },
        },
        ticks: {
          stepSize: 1,
          beginAtZero: true,
        },
      },
    },
  },
});
const clusterGetData = async () => {
  try {
    const std = await fetch(`${domain}/api/dashboard/chart/namestd_of_group`);
    const stdData = await std.json();
    const msv = stdData.data[0];
    const name = stdData.data[1];
    charClusterState.data.labels = name;
    const requests = [];
    for (let i = 0; i < msv.length; i++) {
      const request = await fetch(`${domain}/api/dashboard/chart/stated/group/${msv[i]}`, {
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
    const data = []
    for (let i = 0; i < dataList.length; i++) {
      data.push(dataList[i].data)
    }
    charClusterState.data.datasets[0].data = data;
    if (charClusterState) {
      charClusterState.update()
    }
  }
  catch (error) {
    console.log(error)
  }
}

pieGetData();
lineGetData();
partyGetData();
clusterGetData();
