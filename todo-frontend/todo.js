const userJson = sessionStorage.getItem("user");
const user = JSON.parse(userJson);
const token = sessionStorage.getItem("token");
if (user === null) {
    window.location.href = "home.html";
}

header = document.getElementById("header");
header.innerText = user.username + "'s ToDos";

const logoutButton = document.getElementById("logoutButton");

logoutButton.addEventListener("click", (e) => {
    e.preventDefault();
    console.log(token);
    fetch("http://localhost:5000/logout", { method: "POST",
        headers: {"Content-Type": "application/json",
            "Authorization": `Bearer ${token}`}}).then(response => {
                return response.json();
    }).then(data => {
        if (data.message) {
            alert(data.message);
        }
        sessionStorage.clear();
        window.location.href = "home.html";
    }).catch(error => {
        console.log(error);
        alert(error);
    });

});