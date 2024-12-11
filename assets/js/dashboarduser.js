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
  labels: ["11/12", "12/12", "13/12", "14/12", "15/12"], // Các ngày
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
        title: {
          display: true,
          text: "Trạng thái (1: Đi học, 0: Nghỉ học)", // Tiêu đề trục Y
        },
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

// Render biểu đồ
const ctx = document.getElementById("lineChart").getContext("2d");
new Chart(ctx, lineConfig);

// const lineData = {
//   labels: ["11/12", "12/12", "13/12", "14/12", "15/12"], // Ngày
//   datasets: [
//     {
//       label: "Số buổi đi học",
//       data: [30, 28, 32, 35, 30], // Số lượng
//       borderColor: "#3498db",
//       backgroundColor: "rgba(52, 152, 219, 0.2)",
//       fill: true,
//     },
//     {
//       label: "Số buổi nghỉ học",
//       data: [5, 7, 3, 2, 4], // Số lượng
//       borderColor: "#e74c3c",
//       backgroundColor: "rgba(231, 76, 60, 0.2)",
//       fill: true,
//     },
//   ],
// };

// // Line chart configuration
// const lineConfig = {
//   type: "line",
//   data: lineData,
//   options: {
//     scales: {
//       x: {
//         title: {
//           display: true,
//           text: "Ngày",
//         },
//       },
//       y: {
//         title: {
//           display: true,
//           text: "Số sinh viên",
//         },
//       },
//     },
//   },
// };

// // Render line chart
// new Chart(document.getElementById("lineChart"), lineConfig);
// Biểu đồ đường: Số lần phát biểu
const ctxParticipation = document
  .getElementById("chartParticipation")
  .getContext("2d");
new Chart(ctxParticipation, {
  type: "line",
  data: {
    labels: ["Ngày 1", "Ngày 2", "Ngày 3", "Ngày 4", "Ngày 5"],
    datasets: [
      {
        label: "Số lần phát biểu",
        data: [3, 4, 2, 5, 1],
        borderColor: "#3498db",
        borderWidth: 2,
        fill: false,
        pointBackgroundColor: "#3498db",
        tension: 0.3,
      },
    ],
  },
  options: {
    responsive: true,
  },
});
