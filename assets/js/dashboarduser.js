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
new Chart(pieChart, pieConfig);
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
new Chart(ctx, lineConfig);
const ctxParticipation = document
  .getElementById("chartParticipation")
  .getContext("2d");
new Chart(ctxParticipation, {
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
