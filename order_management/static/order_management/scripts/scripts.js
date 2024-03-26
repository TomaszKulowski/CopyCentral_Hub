function handleDropdownClick(event) {
    event.stopPropagation();
}



$(document).ready(function() {
  $('.executor-select, .region-select, .priority-select').change(function() {
    var selectedValue = $(this).val();
    var selectedType = '';
    if ($(this).hasClass('executor-select')) {
      selectedType = 'executor';
    } else if ($(this).hasClass('region-select')) {
      selectedType = 'region';
    } else if ($(this).hasClass('priority-select')) {
      selectedType = 'priority';
    }
    var orderId = $(this).data('order-id');
    var url = "/orders/" + orderId + "/update/";

    var csrftoken = getCookie('csrftoken');

    var dataToSend = {
      selected_value: selectedValue,
      selected_type: selectedType,
      csrfmiddlewaretoken: csrftoken
    };

    $.ajax({
      url: url,
      type: 'POST',
      data: dataToSend,
      error: function(xhr, textStatus, errorThrown) {
        console.error("Error:", errorThrown);
      }
    });
  });
});



function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
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

var selectedRegion = document.getElementById('filterByRegion').value;
var selectedPriority = document.getElementById('filterByPriority').value;
var selectedExecutor = document.getElementById('filterByEmployee').value;
filterOrders(selectedRegion, selectedPriority, selectedExecutor);


document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.querySelector('.sea');

    searchInput.addEventListener('keyup', function() {
        const searchText = this.value.toLowerCase();
        const rows = document.querySelectorAll('#order-table tr.clickable');

        rows.forEach(function(row) {
            const customerCell = row.querySelector('td:nth-child(2)');
            const customerText = customerCell.textContent.toLowerCase();

            if (customerText.includes(searchText)) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    });
});
