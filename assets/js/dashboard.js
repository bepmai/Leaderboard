function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
  return null;
}

function checkLoginStatus() {
  const token = getCookie('msv');
  console.log(token);
  // if (!token) {
  //   window.location.href = 'sign-in.html';
  // }
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

// Render pie chart
const ctx = document.getElementById("pieChart").getContext("2d");
new Chart(ctx, pieConfig);

const lineData = {
  labels: ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"], // Ngày
  datasets: [
    {
      label: "Số sinh viên đi học",
      data: [],
      borderColor: "#3498db",
      backgroundColor: "rgba(52, 152, 219, 0.2)",
      fill: true,
    },
    {
      label: "Số sinh viên nghỉ học",
      data: [],
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
new Chart(document.getElementById("lineChart"), lineConfig);
// Biểu đồ đường: Số lần phát biểu
const ctxParticipation = document.getElementById('chartParticipation').getContext('2d');
new Chart(ctxParticipation, {
  type: 'line',
  data: {
    labels: ['Ngày 1', 'Ngày 2', 'Ngày 3', 'Ngày 4', 'Ngày 5'],
    datasets: [{
      label: 'Số lần phát biểu',
      data: [3, 4, 2, 5, 1],
      borderColor: '#3498db',
      borderWidth: 2,
      fill: false,
      pointBackgroundColor: '#3498db',
      tension: 0.3
    }]
  },
  options: {
    responsive: true
  }
});

async function fetchChartData() {
  try {
    const response = await fetch('http://localhost:5000/api/chart/data'); // Đường dẫn API của bạn
    const data = await response.json();

    lineData.datasets[0].data = data.attendance;
    lineData.datasets[1].data = data.absence;

    myChart.update();
  } catch (error) {
    console.error('Error fetching data:', error);
  }
}

// Gọi hàm để fetch dữ liệu khi trang được tải
// window.onload = fetchChartData;
