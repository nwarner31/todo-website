const userJson = sessionStorage.getItem("user");
const user = JSON.parse(userJson);
const todosJson = sessionStorage.getItem("todos");
const todos = JSON.parse(todosJson);
const token = sessionStorage.getItem("token");
const newTodoName = document.getElementById("newTodoName");
if (user === null) {
    window.location.href = "home.html";
}

header = document.getElementById("header");
header.innerText = user.username + "'s ToDos";

// Logout Button code
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

// Clear Button code
const clearButton = document.getElementById("clearTodo");

clearButton.addEventListener("click", (e) => {
    e.preventDefault();
    newTodoName.value = "";
})

// Submit ToDo Form code
const todoForm = document.getElementById("createTodo");

todoForm.addEventListener("submit", (e) => {
    e.preventDefault();
    if (newTodoName.value === "") {
        alert("Please enter a name for the ToDo item.");
    } else {
        const body = JSON.stringify({title: newTodoName.value, is_complete: false});
        fetch("http://localhost:5000/todo", {method: "POST", body,
            headers: {"Content-Type": "application/json",
                "Authorization": `Bearer ${token}`}}).then(response => {
                    return response.json();
        }).then(data => {
            if (data.id) {
                addTodoToPage(data);
                todos.push(data);
                sessionStorage.setItem("todos", JSON.stringify(todos));
                newTodoName.value = "";
            }
        });
    }
});


// Add Todo row to the document
function addTodoToPage(todo) {
    function updateTodo(toUpdate) {
        console.log(toUpdate.id);
        console.log(toUpdate.is_complete);
        const body = JSON.stringify({"title": toUpdate.title, "is_complete": toUpdate.is_complete});
        fetch(`http://localhost:5000/todo/${toUpdate.id}`, {method: "PUT", body,
            headers: {"Content-Type": "application/json",
                "Authorization": `Bearer ${token}`}}).then(response => {
                    return response.json();
        }).then(data => {
            if (data.id) {
                let row = document.getElementById(`todo-${data.id}`);
                row.classList.remove("todo-complete");
                row.classList.remove("todo-incomplete");
                let image = document.getElementById(`todo-${data.id}-img`);
                if (data.is_complete) {
                    row.classList.add("todo-complete");
                    image.setAttribute("src", "checkmark.png");
                } else {
                    row.classList.add("todo-incomplete");
                    image.setAttribute("src", "x.png");
                }

                const index = todos.findIndex(item => item.id === data.id);
                todos[index] = data;
                sessionStorage.setItem("todos", JSON.stringify(todos));
            }

        });
    }
    function deleteTodo(toDelete) {
        console.log(toDelete.id);
        fetch(`http://localhost:5000/todo/${toDelete.id}`, {method: "DELETE",
            headers: {"Content-Type": "application/json",
                "Authorization": `Bearer ${token}`}}).then(response => {
                    return response.json();
        }).then(data => {
            if (data.code === 200) {
                const index = todos.indexOf(toDelete);
                todos.splice(index, 1);
                sessionStorage.setItem("todos", JSON.stringify(todos));
                const row = document.getElementById(`todo-${toDelete.id}`);
                row.remove();
            }
        });
    }
    const container = document.createElement("div");
    container.setAttribute("id", `todo-${todo.id}`);
    container.classList.add("todo-item");
    // Status Image
    const statusImage = document.createElement("img");
    statusImage.setAttribute("id", `todo-${todo.id}-img`)
    if (todo.is_complete) {
        container.classList.add("todo-complete")
        statusImage.setAttribute("src", "checkmark.png")
    } else {
        container.classList.add("todo-incomplete");
        statusImage.setAttribute("src", "x.png")
    }
    statusImage.addEventListener("click", (e) => {
        e.preventDefault();
        todo.is_complete = !todo.is_complete
        updateTodo(todo);
    })
    statusImage.classList.add("todo-item-image");
    container.appendChild(statusImage);
    // Todo Text
    const todoText = document.createElement("span");
    todoText.id = `todo-${todo.id}-title`;
    todoText.innerText = todo.title;
    container.appendChild(todoText);

    // Garbage Image
    const garbageImage = document.createElement("img");
    garbageImage.classList.add("todo-item-image");
    garbageImage.classList.add("todo-item-image-right")
    garbageImage.setAttribute("src", "trash.png");
    garbageImage.addEventListener("click", (e) => {
        e.preventDefault();
        deleteTodo(todo);

    })
    container.appendChild(garbageImage);
    // Edit Image
    const editImage = document.createElement("img");
    editImage.classList.add("todo-item-image");
    editImage.classList.add("todo-item-image-right");
    editImage.setAttribute("src", "edit.png");
    editImage.addEventListener("click", (e) => {
        e.preventDefault();
        // Edit Modal
        const modalBg = document.createElement("div");
        modalBg.classList.add("modal-bg");
        const editModal = document.createElement("div");
        editModal.classList.add("edit-modal");
        const editModalHeader = document.createElement("h2");
        editModalHeader.innerText = "Edit Todo";
        editModal.appendChild(editModalHeader);
        const editInputDiv = document.createElement("div");
        const editLabel = document.createElement("label");
        editLabel.innerText = "ToDo Title: ";
        const editInput = document.createElement("input");
        editInput.setAttribute("id", "editInput");
        editLabel.setAttribute("for", "editInput");
        editInput.value = todo.title;
        editInputDiv.appendChild(editLabel);
        editInputDiv.appendChild(editInput);
        editModal.appendChild(editInputDiv);
        const editButtonDiv = document.createElement("div");
        editButtonDiv.classList.add("edit-modal-button-section");
        // Edit Modal: Cancel Button
        const editCancelButton = document.createElement("button");
        editCancelButton.classList.add("edit-modal-button");
        editCancelButton.classList.add("edit-modal-cancel-button");
        editCancelButton.innerText = "Cancel";
        editCancelButton.addEventListener("click", (e) => {
            modalBg.remove();
            editModal.remove();
        });
        editButtonDiv.appendChild(editCancelButton);
        // Edit Modal: Submit Button
        const editSubmitButton = document.createElement("button");
        editSubmitButton.classList.add("edit-modal-button");
        editSubmitButton.innerText = "Submit";
        editSubmitButton.addEventListener("click", (e) => {
            e.preventDefault();
            // Check if the submitted value is the same as the old one
            if (editInput.value !== todo.title) {
                const body = JSON.stringify({title: editInput.value, is_complete: todo.is_complete});
                fetch(`http://localhost:5000/todo/${todo.id}`, {method: "PUT", body,
                    headers: {"Content-Type": "application/json",
                        "Authorization": `Bearer ${token}`}}).then(response => {
                            return response.json();
                }).then(data => {
                    if(data.title) {
                        todoText.innerText = data.title;
                        const index = todos.findIndex(item => item.id === data.id);
                        todos[index] = data;
                        sessionStorage.setItem("todos", JSON.stringify(todos));
                    }

                })
            }
            modalBg.remove();
            editModal.remove();
        })
        editButtonDiv.appendChild(editSubmitButton);
        editModal.appendChild(editButtonDiv);
        modalBg.addEventListener("click", (e) => {
           modalBg.remove();
           editModal.remove();
        });
        const body = document.getElementById("body");
        body.appendChild(modalBg);
        body.appendChild(editModal);

    })
    container.appendChild(editImage);
    const todoHolder = document.getElementById("todoContainer");
    todoHolder.appendChild(container);
}

todos.forEach((todo) => {
    addTodoToPage(todo);

});
