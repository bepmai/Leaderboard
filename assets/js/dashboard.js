
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
    new Chart(document.getElementById("lineChart"), lineConfig);
// Biểu đồ đường: Số lần phát biểu lớp
const ctxParticipation = document.getElementById('chartParticipation').getContext('2d');
new Chart(ctxParticipation, {
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

// Biểu đồ đường: Số lần phát biểu -cụm
const ctxParticipationCluster = document
  .getElementById('chartParticipationCluster')
  .getContext('2d'); 

new Chart(ctxParticipationCluster, {
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

