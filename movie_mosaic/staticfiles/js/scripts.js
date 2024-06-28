// Add star rating movie
const ratingForms = document.querySelectorAll('form[name=rating]');

// Восстановление значения поля формы при загрузке страницы
window.addEventListener('DOMContentLoaded', function() {
    ratingForms.forEach(ratingForm => {
        const movieId = ratingForm.querySelector('input[name=movie]').value;
        const savedStar = localStorage.getItem(`star_${movieId}`);
        if (savedStar) {
            const starInput = ratingForm.querySelector(`input[name=star][value="${savedStar}"]`);
            if (starInput) {
                starInput.checked = true;
            }
        }
    });
});

ratingForms.forEach(ratingForm => {
    ratingForm.addEventListener("change", function (e) {
        // Получаем данные из формы
        let data = new FormData(this);
        const movieId = this.querySelector('input[name=movie]').value;
        fetch(`${this.action}`, {
            method: 'POST',
            body: data,
            headers: {
                'X-CSRFToken': this.querySelector('input[name=csrfmiddlewaretoken]').value
            }
        })
            .then(response => {
                alert("Рейтинг установлен");
                // Сохраняем значение поля в localStorage
                localStorage.setItem(`star_${movieId}`, e.target.value);
            })
            .catch(error => alert("Ошибка"))
    });
});


// Add star rating game
const gameRatingForms = document.querySelectorAll('form[name=rating]');

// Восстановление значения поля формы при загрузке страницы
window.addEventListener('DOMContentLoaded', function() {
    gameRatingForms.forEach(gameRatingForm => {
        const gameId = gameRatingForm.querySelector('input[name=game]').value;
        const savedStar = localStorage.getItem(`game_star_${gameId}`);
        if (savedStar) {
            const starInput = gameRatingForm.querySelector(`input[name=star][value="${savedStar}"]`);
            if (starInput) {
                starInput.checked = true;
            }
        }
    });
});

gameRatingForms.forEach(gameRatingForm => {
    gameRatingForm.addEventListener("change", function (e) {
        // Получаем данные из формы
        let data = new FormData(this);
        const gameId = this.querySelector('input[name=game]').value;
        fetch(`${this.action}`, {
            method: 'POST',
            body: data,
            headers: {
                'X-CSRFToken': this.querySelector('input[name=csrfmiddlewaretoken]').value
            }
        })
        .then(response => {
            if (response.ok) {
                alert("Рейтинг установлен");
                // Сохраняем значение поля в localStorage
                localStorage.setItem(`game_star_${gameId}`, e.target.value);
            } else {
                alert("Ошибка при установке рейтинга");
            }
        })
        .catch(error => alert("Ошибка"));
    });
});


// Add star rating serial
const serialRatingForms = document.querySelectorAll('form[name=rating]');

// Восстановление значения поля формы при загрузке страницы
window.addEventListener('DOMContentLoaded', function() {
    serialRatingForms.forEach(serialRatingForm => {
        const serialId = serialRatingForm.querySelector('input[name=serial]').value;
        const savedStar = localStorage.getItem(`serial_star_${serialId}`);
        if (savedStar) {
            const starInput = serialRatingForm.querySelector(`input[name=star][value="${savedStar}"]`);
            if (starInput) {
                starInput.checked = true;
            }
        }
    });
});

serialRatingForms.forEach(serialRatingForm => {
    serialRatingForm.addEventListener("change", function (e) {
        // Получаем данные из формы
        let data = new FormData(this);
        const serialId = this.querySelector('input[name=serial]').value;
        fetch(`${this.action}`, {
            method: 'POST',
            body: data,
            headers: {
                'X-CSRFToken': this.querySelector('input[name=csrfmiddlewaretoken]').value
            }
        })
        .then(response => {
            if (response.ok) {
                alert("Рейтинг установлен");
                // Сохраняем значение поля в localStorage
                localStorage.setItem(`serial_star_${serialId}`, e.target.value);
            } else {
                alert("Ошибка при установке рейтинга");
            }
        })
        .catch(error => alert("Ошибка"));
    });
});



// Загрузка изображения обложки и применение его в качестве фона
const movieCover = document.getElementById('video-cover');
const blurBackground = document.querySelector('.blur-background');

movieCover.addEventListener('load', function() {
    blurBackground.style.setProperty('--cover-background', `url(${movieCover.src})`);
});


// Поиск
