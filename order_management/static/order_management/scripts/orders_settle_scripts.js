function toggleDetails(orderId) {
    var detailsRow = document.getElementById('row' + orderId);
    detailsRow.classList.toggle('show');
}