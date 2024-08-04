document.getElementById('filterByStatus').addEventListener('change', handleFilterChange);
document.getElementById('filterByRegion').addEventListener('change', handleFilterChange);
document.getElementById('filterByPriority').addEventListener('change', handleFilterChange);
document.getElementById('filterByEmployee').addEventListener('change', handleFilterChange);

function handleFilterChange() {
    var selectedStatus = document.getElementById('filterByStatus').value;
    var selectedRegion = document.getElementById('filterByRegion').value;
    var selectedPriority = document.getElementById('filterByPriority').value;
    var selectedExecutor = document.getElementById('filterByEmployee').value;
    filterOrders(selectedStatus, selectedRegion, selectedPriority, selectedExecutor);
}

function filterOrders(selectedStatus, selectedRegion, selectedPriority, selectedExecutor) {
    var rows = document.querySelectorAll('#order-table tr.clickable');
    rows.forEach(function(row) {
        var detailsRowId = row.getAttribute('data-target').substring(1);
        var detailsRow = document.getElementById(detailsRowId);

        var statusCell = row.querySelector('td:nth-child(9)');
        var regionCell = row.querySelector('td:nth-child(10) select');
        var priorityCell = row.querySelector('td:nth-child(11) select');
        var executorCell = row.querySelector('td:nth-child(12) select');

        var statusValue = statusCell ? statusCell.getAttribute('data-status-id') : 'All';
        var regionValue = regionCell ? regionCell.value : 'Display All';
        var priorityValue = priorityCell ? priorityCell.value : 'All';
        var executorValue = executorCell ? executorCell.value : 'All';

        var statusMatch = selectedStatus === 'All' || statusValue === selectedStatus;
        var regionMatch = selectedRegion === 'Display All' || regionValue === selectedRegion;
        var priorityMatch = selectedPriority === 'All' || priorityValue === selectedPriority;
        var executorMatch = selectedExecutor === 'All' || executorValue === selectedExecutor;

        if (statusMatch && regionMatch && priorityMatch && executorMatch) {
            row.style.display = '';
            if (detailsRow) {
                detailsRow.style.display = '';
            }
        } else {
            row.style.display = 'none';
            if (detailsRow) {
                detailsRow.style.display = 'none';
            }
        }
    });

    $.ajax({
        url: "apply_filters/?region=" + selectedRegion,
        type: 'GET',
    });
}

handleFilterChange();
