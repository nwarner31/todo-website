let registerForm = document.getElementById("registerForm");

registerForm.addEventListener("submit", (e) => {
    e.preventDefault();
    let username = document.getElementById("username");
    let password = document.getElementById("password");
    const page = document.getElementById("body");
    const errorToast = document.createElement("div");
    errorToast.classList.add("toast");
    errorToast.classList.add("red-toast");
    if (username.value === "" || password.value.length < 6) {
        errorToast.innerText = "Please enter a username and a password of at least 6 characters long.";
        page.appendChild(errorToast);
        setTimeout(() => {
            errorToast.remove();
        }, 3000);
    } else {
        const body = JSON.stringify({username: username.value, password: password.value});
        fetch( "http://localhost:5000/register", {method: "POST", body,
            headers: {"Content-Type": "application/json"}}).then(response => {
                return response.json();
        }).then(data => {
            console.log(data);
            if (data.user) {
                console.log("Have user");
                const user = data.user;
                sessionStorage.setItem("todos", JSON.stringify(data.todos));
                delete user.todos;
                sessionStorage.setItem("user", JSON.stringify(user));
                sessionStorage.setItem("token", data.token);
                window.location.href = "todo.html";
            } else {
                errorToast.innerText = "Username unavailable.";
                page.appendChild(errorToast);
                setTimeout(() => {
                    errorToast.remove();
                }, 3000);
            }
        })
    }
})