// JavaScript для открытия и закрытия модального окна
const modal = document.getElementById("modal");
const btn = document.getElementById("edit-button");
const close = document.getElementsByClassName("close")[0];
const saveChanges = document.getElementById("save-changes");

btn.onclick = function() {
    modal.style.display = "block";
}

close.onclick = function() {
    modal.style.display = "none";
}

window.onclick = function(event) {
    if (event.target === modal) {
        modal.style.display = "none";
    }
}

saveChanges.onclick = function() {
    // Логика для сохранения изменений
    alert("Изменения сохранены!");
    modal.style.display = "none";
}
