let user = document.getElementById("user")
    editUserButton = document.getElementsByClassName("warning")
    deleteUserButton = document.getElementsByClassName("danger")

for (let i = 0; i < editUserButton.length; i++) {
    let element = editUserButton[i];
    element.addEventListener('click', edit);
}

for (let i = 0; i < deleteUserButton.length; i++) {
    let element = deleteUserButton[i];
    element.addEventListener('click', remove);
}

function remove() {

}

function edit() {

}