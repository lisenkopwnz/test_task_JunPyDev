document.addEventListener('DOMContentLoaded', function() {
    // контейнер для форм и кнопку добавления
    const formContainer = document.querySelector('#form-container');
    const addButton = document.querySelector('#add-form');

    // скрытое поле с общим количеством форм
    const totalForms = document.querySelector('#id_order_dishes-TOTAL_FORMS');

    // Если поле не найдено, выполнение завершается
    if (!totalForms) {
        return;
    }

    // Получаею текущее количество форм
    let formCount = parseInt(totalForms.value);

    // Удаляю пустой вариант из выпадающего списка
    function removeEmptyOption(selectElement) {
        if (selectElement && selectElement.options.length > 0 && selectElement.options[0].text === '---------') {
            selectElement.remove(0);
        }
    }

    // Применяем функцию ко всем выпадающим спискам
    document.querySelectorAll('.dish-form select').forEach(select => {
        removeEmptyOption(select);
    });

    // Обработчик для кнопки добавления новой формы
    addButton.addEventListener('click', function() {
        // Клонируем первую форму
        const newForm = formContainer.querySelector('.dish-form').cloneNode(true);

        // Обновляю имена и ID полей в новой форме
        newForm.innerHTML = newForm.innerHTML.replace(/order_dishes-\d+/g, `order_dishes-${formCount}`);

        // Добавляю новую форму в контейнер
        formContainer.appendChild(newForm);

        // Убираем пустой вариант из нового выпадающего списка
        const newSelect = newForm.querySelector('select');
        removeEmptyOption(newSelect);

        // Увеличиваю счетчик форм
        formCount += 1;
        totalForms.value = formCount;
    });
});
