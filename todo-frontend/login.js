let loginForm = document.getElementById("loginForm");

loginForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const username = document.getElementById("username");
    const password = document.getElementById("password");
    const errorToast = document.createElement("div");
    const page = document.getElementById("body");
    errorToast.classList.add("toast");
    errorToast.classList.add("red-toast");
    if (username.value === "" || password.value === "") {
        errorToast.innerText = "Please enter a username and a password.";
        page.appendChild(errorToast);
        setTimeout(() => {
            errorToast.remove();
        }, 3000);
    } else {
        const body = JSON.stringify({username: username.value, password: password.value});
        fetch("http://localhost:5000/login", {method: "POST", body,
            headers: {"Content-Type": "application/json"}}).then(response => {
                return response.json();
        }).then(data => {
            if(data.user) {
                console.log(data.user);
                const user = data.user;
                sessionStorage.setItem("todos", JSON.stringify(user.todos));
                delete user.todos;
                sessionStorage.setItem("user", JSON.stringify(user));
                sessionStorage.setItem("token", data.token);
                window.location.href = "todo.html";
            } else {
                console.log(data);
                errorToast.innerText = "There was a problem logging in";
                page.appendChild(errorToast);
                setTimeout(() => {
                    errorToast.remove();
                }, 3000);
            }

        })
    }
})

