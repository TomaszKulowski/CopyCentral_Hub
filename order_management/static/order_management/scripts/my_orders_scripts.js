$(document).ready(function() {
    $('#filterByRegion').on('change', function() {
        var selectedRegion = $(this).val();
        if(selectedRegion === 'Display All') {
            $('.region-table').show();
        } else {
            $('.region-table').hide();
            $('.' + selectedRegion).show();
        }
        $.ajax({
            url: "/order_management/apply_filters/?region=" + selectedRegion,
            type: 'GET',
        });
    });
});


function initFilters() {
    var selectedRegion = document.getElementById('filterByRegion').value;
    var selectedPriority = document.getElementById('filterByPriority').value;
    var selectedExecutor = document.getElementById('filterByEmployee').value;
    filterOrders(selectedRegion, selectedPriority, selectedExecutor);
}

document.getElementById('filterByRegion').addEventListener('change', function() {
    var selectedRegion = this.value;
    var selectedExecutor = document.getElementById('filterByEmployee').value;
});


initFilters();
