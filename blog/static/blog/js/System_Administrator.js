// Открытие модального окна
function openModal() {
    document.getElementById('modal').style.display = 'block';
}

// Закрытие модального окна
function closeModal() {
    document.getElementById('modal').style.display = 'none';
}

// Добавление нового кассира
function addCashier() {
    const surname = document.getElementById('surname').value;
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const login = document.getElementById('login').value;
    const password = document.getElementById('password').value;

    const data = {
        surname: surname,
        name: name,
        email: email,
        login: login,
        password: password
    };

    fetch('/add_cashier/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Кассир добавлен успешно!');
            closeModal();
        } else {
            alert('Ошибка при добавлении кассира: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
        alert('Ошибка при отправке данных.');
    });
}

// Получение CSRF токена
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Привязка функций к кнопкам
document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('.registration').addEventListener('click', openModal);
    document.querySelector('.submit-button').addEventListener('click', addCashier);
});

