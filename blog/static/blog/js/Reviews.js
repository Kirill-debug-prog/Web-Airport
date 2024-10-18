document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById("review-modal");
    const btn = document.querySelector(".button-text");
    const span = document.querySelector(".close-button");
    const submitReviewButton = document.getElementById("submit-review");

    btn.onclick = function() {
        modal.style.display = "block";
    }

    span.onclick = function() {
        modal.style.display = "none";
    }

    submitReviewButton.addEventListener("click", () => {
        const name = document.getElementById("name").value;
        const reviewText = document.getElementById("review-text").value;

        if (!reviewText) {
            alert('Пожалуйста, напишите отзыв.');
            return;
        }

        const formData = new FormData();
        formData.append('name', name);
        formData.append('review_text', reviewText);

        fetch('/add_review/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                createReviewElement(name, reviewText);
                modal.style.display = "none";
                document.getElementById("name").value = '';
                document.getElementById("review-text").value = '';
            } else {
                alert('Не удалось добавить отзыв: ' + (data.message || 'Ошибка валидации'));
            }
        });
    });
});

function createReviewElement(name, reviewText) {
    const reviewsContainer = document.querySelector(".reviews-container");
    const reviewGroup = document.createElement("div");
    reviewGroup.className = "review-group";

    const reviewRectangle = document.createElement("div");
    reviewRectangle.className = "review-rectangle";

    const reviewName = document.createElement("p");
    reviewName.className = "review-name";
    reviewName.textContent = name;

    const reviewTextElement = document.createElement("p");
    reviewTextElement.className = "review-text";
    reviewTextElement.textContent = reviewText;

    reviewRectangle.appendChild(reviewName);
    reviewRectangle.appendChild(reviewTextElement);

    reviewGroup.appendChild(reviewRectangle);
    reviewsContainer.appendChild(reviewGroup);
}

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
