let registerForm = document.getElementById("registerForm");

registerForm.addEventListener("submit", (e) => {
    e.preventDefault();
    let username = document.getElementById("username");
    let password = document.getElementById("password");

    if (username.value === "" || password.value.length < 6) {
        alert("Please enter a valid username and password");
    } else {
        const body = JSON.stringify({username: username.value, password: password.value});
        fetch( "http://localhost:5000/register", {method: "POST", body,
            headers: {"Content-Type": "application/json"}}).then(response => {
                return response.json();
        }).then(data => {
            console.log(data);
            if (data.user) {
                console.log("Have user");
            } else {
                alert("There was an error")
            }
        })
    }
})