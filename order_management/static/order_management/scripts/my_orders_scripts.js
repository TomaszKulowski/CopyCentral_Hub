$(document).ready(function() {
    function applyFilters() {
        var selectedRegion = $('#filterByRegion').val();
        if (selectedRegion === 'Display All') {
            $('.region-table').show();
        } else {
            $('.region-table').hide();
            $('.' + selectedRegion).show();
        }
        $.ajax({
            url: "/order_management/apply_filters/?region=" + selectedRegion,
            type: 'GET',
        });
    }

    applyFilters();

    $('#filterByRegion').on('change', function() {
        applyFilters();
    });
});
