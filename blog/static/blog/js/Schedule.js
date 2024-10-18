document.addEventListener('DOMContentLoaded', function() {
    function loadSchedule(scheduleType) {
        $.ajax({
            url: `/api/schedule/${scheduleType}/`,
            method: 'GET',
            success: function(data) {
                const tableBody = $('#schedule-table-body');
                tableBody.empty();
                if (data.length === 0) {
                    $('#no-flights-message').show();
                } else {
                    $('#no-flights-message').hide();
                    data.forEach(function(schedule) {
                        const row = `
                            <tr>
                                <td>${schedule.flight_number}</td>
                                <td>${schedule.route}</td>
                                <td>${schedule.airline_id}</td>
                                <td>${schedule.arrival_date || schedule.departure_date} ${schedule.arrival_time || schedule.departure_time}</td>
                                <td>${schedule.transport_model}</td>
                            </tr>
                        `;
                        tableBody.append(row);
                    });
                }
            },
            error: function() {
                console.error('Ошибка загрузки данных');
            }
        });
    }

    // Загрузить расписание по умолчанию
    loadSchedule('departure');

    // Обработка переключения фильтров
    $('input[name="flight_type"]').on('change', function() {
        const selectedType = $('input[name="flight_type"]:checked').attr('id') === 'Arrival_to_Vladivostok' ? 'arrival' : 'departure';
        loadSchedule(selectedType);
    });
});

document.addEventListener('DOMContentLoaded', function() {
    // Функция для загрузки расписания с учетом фильтров
    function loadSchedule(scheduleType, filters = {}) {
        const queryString = $.param(filters);  // Преобразует объект фильтров в строку запроса
        const url = `/api/schedule/${scheduleType}/?${queryString}`;

        $.ajax({
            url: url,
            method: 'GET',
            success: function(data) {
                const tableBody = $('#schedule-table-body');
                tableBody.empty();
                if (data.length === 0) {
                    $('#no-flights-message').show();
                } else {
                    $('#no-flights-message').hide();
                    data.forEach(function(schedule) {
                        const row = `
                            <tr>
                                <td>${schedule.flight_number}</td>
                                <td>${schedule.route}</td>
                                <td>${schedule.airline_id}</td>
                                <td>${schedule.arrival_date || schedule.departure_date} ${schedule.arrival_time || schedule.departure_time}</td>
                                <td>${schedule.transport_model}</td>
                            </tr>
                        `;
                        tableBody.append(row);
                    });
                }
            },
            error: function() {
                console.error('Ошибка загрузки данных');
            }
        });
    }

    // Функция для сбора данных фильтров
    function getFilters() {
        const flightType = $('input[name="flight_type"]:checked').attr('id') === 'Arrival_to_Vladivostok' ? 'arrival' : 'departure';
        const airline = $('#airline-filter').val();  // Пример получения значения из выпадающего списка
        const dateFrom = $('#date-from').val();  // Пример получения значения из поля ввода
        const dateTo = $('#date-to').val();  // Пример получения значения из поля ввода

        return {
            flightType: flightType,
            airline: airline,
            date_from: dateFrom,
            date_to: dateTo
        };
    }

    // Загрузить расписание по умолчанию
    loadSchedule('departure');

    // Обработка переключения фильтров
    $('input[name="flight_type"]').on('change', function() {
        const filters = getFilters();
        loadSchedule(filters.flightType, filters);
    });

    // Обработка изменений других фильтров
    $('#airline-filter, #date-from, #date-to').on('change', function() {
        const filters = getFilters();
        loadSchedule(filters.flightType, filters);
    });
});

$(document).ready(function() {
    // При нажатии на радиокнопку выбора направления
    $('.schedule-filters__item-option-input').change(function() {
        // Удаляем класс выделения у всех элементов
        $('.schedule-filters__item-option').removeClass('schedule-filters__item-option--selected');
        
        // Добавляем класс выделения только к выбранному элементу
        $(this).closest('.schedule-filters__item-option').addClass('schedule-filters__item-option--selected');
        
        // Обновляем текст выбранного элемента
        var selectedText = $(this).next('label').text();
        $(this).closest('.schedule-filters').find('.schedule-filters__item-selected-text').text(selectedText);
    });
});
