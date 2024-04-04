document.getElementById('filterByRegion').addEventListener('change', function() {
    var selectedRegion = this.value;
    var selectedPriority = document.getElementById('filterByPriority').value;
    var selectedExecutor = document.getElementById('filterByEmployee').value;
    filterOrders(selectedRegion, selectedPriority, selectedExecutor);
});

document.getElementById('filterByPriority').addEventListener('change', function() {
    var selectedRegion = document.getElementById('filterByRegion').value;
    var selectedPriority = this.value;
    var selectedExecutor = document.getElementById('filterByEmployee').value;
    filterOrders(selectedRegion, selectedPriority, selectedExecutor);
});

document.getElementById('filterByEmployee').addEventListener('change', function() {
    var selectedRegion = document.getElementById('filterByRegion').value;
    var selectedPriority = document.getElementById('filterByPriority').value;
    var selectedExecutor = this.value;
    filterOrders(selectedRegion, selectedPriority, selectedExecutor);
});


function filterOrders(selectedRegion, selectedPriority, selectedExecutor) {
    var rows = document.querySelectorAll('#order-table tr.clickable');
    rows.forEach(function(row) {
        var priorityCell = row.querySelector('td:nth-child(8) select');
        var executorCell = row.querySelector('td:nth-child(9) select');
        var regionCell = row.querySelector('td:nth-child(7) select');

        var priorityValue = priorityCell ? priorityCell.value : 'All';
        var executorValue = executorCell ? executorCell.value : 'All';
        var regionValue = regionCell ? regionCell.value : 'Display All';

        var regionMatch = selectedRegion === 'Display All' || regionValue === selectedRegion;
        var priorityMatch = selectedPriority === 'All' || priorityValue === selectedPriority;
        var executorMatch = selectedExecutor === 'All' || executorValue === selectedExecutor;

        if (regionMatch && priorityMatch && executorMatch) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });

    $.ajax({
        url: "apply_filters/?region=" + selectedRegion,
        type: 'GET',
    });
}

function initFilters() {
    var selectedRegion = document.getElementById('filterByRegion').value;
    var selectedPriority = document.getElementById('filterByPriority').value;
    var selectedExecutor = document.getElementById('filterByEmployee').value;
    filterOrders(selectedRegion, selectedPriority, selectedExecutor);
}

document.getElementById('filterByRegion').addEventListener('change', function() {
    var selectedRegion = this.value;
    var selectedPriority = document.getElementById('filterByPriority').value;
    var selectedExecutor = document.getElementById('filterByEmployee').value;
    filterOrders(selectedRegion, selectedPriority, selectedExecutor);
});

document.getElementById('filterByPriority').addEventListener('change', function() {
    var selectedRegion = document.getElementById('filterByRegion').value;
    var selectedPriority = this.value;
    var selectedExecutor = document.getElementById('filterByEmployee').value;
    filterOrders(selectedRegion, selectedPriority, selectedExecutor);
});

document.getElementById('filterByEmployee').addEventListener('change', function() {
    var selectedRegion = document.getElementById('filterByRegion').value;
    var selectedPriority = document.getElementById('filterByPriority').value;
    var selectedExecutor = this.value;
    filterOrders(selectedRegion, selectedPriority, selectedExecutor);
});

initFilters();