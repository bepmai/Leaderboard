const username = document.getElementById("username");
const password = document.getElementById("password");

async function login(event) {
    const loginData = {
        username: username.value,
        password: password.value
    };

    try {
        const response = await fetch(`${domain}/api/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(loginData),
            credentials: 'include'
        });
        if (response.ok) {
            const result = await response.json();
            const res = await fetch(`${domain}/api/auth/role`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(loginData),
                credentials: 'include'
            });
            if(res.ok){
                if(getCookie("role")=="admin"){
                    window.location.href="dashboard"
                }
                else{
                    window.location.href="dashboarduser"
                }
                console.log(document.cookie)
            }
        } else {
            const error = await response.json();
            console.log(error)
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred. Please try again later.');
    }
}
