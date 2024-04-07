function handleDropdownClick(event) {
    event.stopPropagation();
}


function handleMoveButtonClick(event, direction) {
    event.stopPropagation();
    event.preventDefault();

    var button = event.target;
    var row = button.closest('tr');
    var orderId = row.getAttribute('data-order_id');
    var executorId = row.getAttribute('data-executor_id');
    var tableId = row.getAttribute('data-table_id');
    var currentPosition = row.getAttribute('data-current_position');
    var newPosition = direction === 'up' ? parseInt(currentPosition) - 1 : parseInt(currentPosition) + 1;
    var csrftoken = getCookie('csrftoken');
    var url = "/orders/api/" + orderId + "/sort_number_update/";

    var dataToSend = {
        order_id: orderId,
        table_id: tableId,
        executor_id: executorId,
        current_position: currentPosition,
        new_position: newPosition,
        csrfmiddlewaretoken: csrftoken
    };

    $.ajax({
        url: url,
        type: 'POST',
        data: dataToSend,
        success: function(response) {
        $('#order-table-' + tableId).html(response);
        },
        error: function(xhr, textStatus, errorThrown) {
            console.error("Error:", errorThrown);
        }
    });

}

document.addEventListener('click', function(event) {
    var button = event.target.closest('.move-up, .move-down');
    if (button) {
        var direction = button.classList.contains('move-up') ? 'up' : 'down';
        handleMoveButtonClick(event, direction);
    }
});
