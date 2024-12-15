if (getCookie('token') == null) {
    window.location.href = "/"
}
const userattend = document.getElementById("attendance-user")
const adminattend = document.getElementById("attendance-admin")
const stated = document.getElementById("stated-user")
const tongquan = document.getElementById("tongquan")
const socket = io();

function joinRoom() {
    if (getCookie('msv')) {
        socket.emit('join', { 'msv': getCookie('msv') });
    }
}

joinRoom();

if (getCookie('role') == "admin") {
}
else {
    adminattend.classList.add("hidden")
    stated.classList.add("hidden")
    tongquan.classList.add("hidden")
}
const ranking = document.getElementById("ranking");
const getDataRanking = async () => {
    try {
        const response = await fetch(`${domain}/api/leaderboard/getLeaderClass`,{
            credentials:'include'
        });
        const data = await response.json();
        const rows = []
        for (let index = 0; index < data.data.length; index++) {
            const member = data.data[index];
            const row = document.createElement('tr');

            const rankCell = document.createElement('td');
            let rankIcon;
            if (index === 0) {
                rankIcon = document.createElement('i');
                rankIcon.classList.add('fas', 'fa-trophy', 'trophy-icon', 'gold');
                rankIcon.style.color = 'gold';
            } else if (index === 1) {
                rankIcon = document.createElement('i');
                rankIcon.classList.add('fas', 'fa-trophy', 'trophy-icon', 'silver');
                rankIcon.style.color = 'silver';
            } else if (index === 2) {
                rankIcon = document.createElement('i');
                rankIcon.classList.add('fas', 'fa-trophy', 'trophy-icon', 'bronze');
                rankIcon.style.color = '#cd7f32'; // Màu đồng
            } else {
                rankIcon = document.createTextNode(index + 1); // Thứ hạng bình thường
            }

            rankCell.appendChild(rankIcon);

            const nameCell = document.createElement('td');
            nameCell.textContent = member.first_name + " " + member.last_name;

            const attendanceCell = document.createElement('td');
            attendanceCell.textContent = 15 - member.absent;

            const speechScoreCell = document.createElement('td');
            speechScoreCell.textContent = member.volunteer_class;

            const projectScoreCell = document.createElement('td');
            projectScoreCell.textContent = member.project_class;

            const totalScoreCell = document.createElement('td');
            totalScoreCell.textContent = member.point_class;

            row.appendChild(rankCell);
            row.appendChild(nameCell);
            row.appendChild(attendanceCell);
            row.appendChild(speechScoreCell);
            row.appendChild(projectScoreCell);
            row.appendChild(totalScoreCell);

            rows.push(row);
        };
        rows.forEach(row => {
            ranking.appendChild(row);
        })
    }
    catch (error) {
        console.log(error)
    }
}
getDataRanking()
socket.on('receive_data', function (data) {
    console.log('receive_data')
    getDataRanking()
});
