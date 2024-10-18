document.querySelector('.search-button').addEventListener('click', function() {
    var lastName = document.querySelector('.input-container').value;

    // AJAX запрос на сервер для поиска кассира
    fetch(`/search_cashier/?last_name=${lastName}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                document.getElementById('last-name').textContent = 'Фамилия: ' + data.last_name;
                document.getElementById('first-name').textContent = 'Имя: ' + data.first_name;
                document.getElementById('email').textContent = 'Email: ' + data.email;
                document.getElementById('login').textContent = 'Логин: ' + data.username;
                document.getElementById('date-joined').textContent = 'Дата регистрации: ' + data.date_joined;
            }
        });
});
