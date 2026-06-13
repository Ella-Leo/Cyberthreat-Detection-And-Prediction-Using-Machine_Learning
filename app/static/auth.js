function registerUser() {
    let username = document.querySelector("#reg-username").value;
    let password = document.querySelector("#reg-password").value;
    let role = document.querySelector("#role").value;

    fetch("/register", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username,
            password,
            role
        })
    })
    .then(res => res.json())
    .then(data => {
        alert(data.message);
    });
}


function loginUser() {
    let username = document.querySelector("#login-username").value;
    let password = document.querySelector("#login-password").value;

    fetch("/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username,
            password
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.token) {
            localStorage.setItem("token", data.token);
window.location.href = "http://localhost:8501";l
        } else {
            alert(data.message);
        }
    });
}