$(document).ready(function() {
    let orderIdToDelete;

    // Открытие модального окна и сохранение id заказа
    $('.delete-btn').click(function() {
        orderIdToDelete = $(this).data('order-id');
    });

    // Подтверждение удаления
    $('#confirmDelete').click(function() {
        const url = `/order/delete_order/${orderIdToDelete}/`;

        $.ajax({
            url: url,
            method: 'POST',
            headers: {
                'X-CSRFToken': $('meta[name="csrf-token"]').attr('content'),
            },
            success: function() {
                $('#deleteModal').modal('hide');
                $(`#order-${orderIdToDelete}`).remove();
                showToast('Заказ успешно удалён.', 'success');
            },
            error: function(xhr) {
                $('#deleteModal').modal('hide');
                if (xhr.status === 404) {
                    showToast('Заказ не найден.', 'danger');
                } else {
                    showToast('Произошла ошибка при удалении заказа.', 'danger');
                }
            }
        });
    });

    // Изменение статуса
    $('.change-status').click(function(e) {
        e.preventDefault();

        const orderId = $(this).data('order-id');
        const newStatus = $(this).data('status');

        $.ajax({
            url: `/order/update-status/${orderId}/`,
            method: 'POST',
            headers: {
                'X-CSRFToken': $('meta[name="csrf-token"]').attr('content'),
            },
            data: {
                status: newStatus,
            },
            success: function(data) {
                if (data.status === 'success') {
                    const statusDisplay = {
                        'pending': 'В ожидании',
                        'ready': 'Готово',
                        'paid': 'Оплачено'
                    };
                    $(`#dropdownMenuButton${orderId}`).text(statusDisplay[newStatus]);
                    $(`#order-${orderId} td:nth-child(5)`).text(statusDisplay[newStatus]);
                    showToast('Статус успешно изменён.', 'success');
                } else {
                    showToast('Ошибка: ' + data.message, 'danger');
                }
            },
            error: function(error) {
                showToast('Произошла ошибка при изменении статуса.', 'danger');
            }
        });
    });

    // Проверка номера стола перед отправкой
    $('#searchForm').submit(function(e) {
        const tableNumber = $('#table_number').val();
        if (tableNumber && isNaN(tableNumber)) {
            e.preventDefault();  // Остановить отправку формы
            showToast('Номер стола должен быть числом.', 'danger');
        }
    });

    // Функция для показа уведомлений
    function showToast(message, type) {
        const toastTemplate = $('#toastTemplate').clone().removeAttr('id');
        toastTemplate.find('.toast-body').text(message);
        toastTemplate.addClass(`bg-${type} text-white`);
        toastTemplate.appendTo('#toastContainer');
        const toast = new bootstrap.Toast(toastTemplate[0]);
        toast.show();
        toastTemplate.on('hidden.bs.toast', function() {
            $(this).remove();
        });
    }
});
