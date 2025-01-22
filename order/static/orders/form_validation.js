(function () {
    'use strict'

    // Получаю форму
    const form = document.querySelector('.needs-validation')

    // обработчик события submit
    form.addEventListener('submit', function (event) {
        if (!form.checkValidity()) {
            event.preventDefault()
            event.stopPropagation()
        }

        form.classList.add('was-validated')
    }, false)
})()