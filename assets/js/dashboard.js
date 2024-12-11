// Biểu đồ tròn: Số buổi đi học
const ctxAttendance = document.getElementById('pieChart').getContext('2d');
new Chart(ctxAttendance, {
    type: 'pie',
    data: {
        labels: ['Đi học', 'Nghỉ'],
        datasets: [{
            data: [30, 5],
            backgroundColor: ['#2ecc71', '#e74c3c'],
        }]
    },
    options: {
        responsive: true
    }
});

// Biểu đồ cột: Số buổi nghỉ
const ctxAbsences = document.getElementById('chartAbsences').getContext('2d');
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
