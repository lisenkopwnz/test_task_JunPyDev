$(document).ready(function () {
    let dishIdToDelete = null;

    // Обработка клика по кнопке "Удалить"
    $('.delete-dish').on('click', function () {
        dishIdToDelete = $(this).data('dish-id');
        $('#deleteDishModal').modal('show');
    });

    // Обработка подтверждения удаления
    $('#confirmDeleteDish').on('click', function () {
        if (dishIdToDelete) {
            $.ajax({
                url: `/order/delete_dish/${dishIdToDelete}/`,  // URL для удаления блюда
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': $('meta[name="csrf-token"]').attr('content')  // CSRF-токен для защиты
                },
                success: function (response) {
                    $('#deleteDishModal').modal('hide');
                    showToast('Блюдо успешно удалено!', 'success');
                    $(`#dish-${dishIdToDelete}`).remove();  // Удаляем строку из таблицы
                },
                error: function (xhr) {
                    $('#deleteDishModal').modal('hide');
                    showToast('Ошибка при удалении блюда.', 'danger');
                }
            });
        }
    });

    // Функция для отображения уведомлений
    function showToast(message, type) {
        const toastTemplate = $('#toastTemplate').clone().removeAttr('id');
        toastTemplate.find('.toast-body').text(message);
        toastTemplate.addClass(`bg-${type}`);

        $('#toastContainer').append(toastTemplate);
        toastTemplate.toast('show');

        toastTemplate.on('hidden.bs.toast', function () {
            toastTemplate.remove();
        });
    }
});