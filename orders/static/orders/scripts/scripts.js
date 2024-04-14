document.addEventListener("DOMContentLoaded", function () {
    var tableBody = document.getElementById("table-body");
    if (tableBody) {
        tableBody.addEventListener("click", function(event) {
            var target = event.target.closest("tr");
            if (target) {
                var url = target.querySelector("td:first-child").textContent;
                window.location.href = url;
            }
        });
    }

    var searchInput = document.querySelector(".sea");
    var previousSearchQuery = "";

    searchInput.addEventListener("input", function () {
        clearTimeout(this.typingTimer);
        this.typingTimer = setTimeout(function () {
            sendSearchRequest();
        }, 300); // Adjust this interval as needed
    });

    // Add keydown event listener to the search input
    searchInput.addEventListener("keydown", function (event) {
        // Prevent the default action if Enter key is pressed
        if (event.key === 'Enter') {
            event.preventDefault();
        }
    });

    function sendSearchRequest() {
        var searchQuery = searchInput.value.trim();

        // Check if the searchQuery is different from the previous search
        if (searchQuery !== previousSearchQuery) {
            var url = "/orders/?search=";


            // Append the search parameter only if the searchQuery is not empty
            if (searchQuery !== "") {
                url += `${encodeURIComponent(searchQuery)}`;
            }

            fetch(url)
                .then(response => response.text())
                .then(data => {
                    document.getElementById("table-body").innerHTML = data;
                    document.getElementById("paginator").innerHTML = '';

                    // Update the previous searchQuery
                    previousSearchQuery = searchQuery;
                })
                .catch(error => {
                    console.error("Error:", error);
                });
        }
    }
});


$(document).ready(function() {
    $('#id_customer').on('select2:select', function (e) {
        var customerId = e.params.data.id;
        var orderId = $('#orderId').val();
        var payerId = $('#payerId').val();
        var addressId = $('#addressId').val();

        window.location.href = '/orders/' + orderId + '/update/?customer_id=' + customerId + '&payer_id=' + payerId + '&address_id=' + addressId;
    });
});

$(document).ready(function() {
    $('#id_payer').on('select2:select', function (e) {
        var payerId = e.params.data.id;
        var orderId = $('#orderId').val();
        var customerId = $('#customerId').val();
        var addressId = $('#addressId').val();

        window.location.href = '/orders/' + orderId + '/update/?customer_id=' + customerId + '&payer_id=' + payerId + '&address_id=' + addressId;
    });
});

$(document).ready(function() {
    $('#id_address').on('select2:select', function (e) {
        var addressId = e.params.data.id;
        var orderId = $('#orderId').val();
        var customerId = $('#customerId').val();
        var payerId = $('#payerId').val();

        window.location.href = '/orders/' + orderId + '/update/?customer_id=' + customerId + '&payer_id=' + payerId + '&address_id=' + addressId;
    }).on('select2:unselect', function (e) {
        var addressId = null;
        var orderId = $('#orderId').val();
        var customerId = $('#customerId').val();
        var payerId = $('#payerId').val();

        window.location.href = '/orders/' + orderId + '/update/?customer_id=' + customerId + '&payer_id=' + payerId + '&address_id=' + addressId;
    });
});


function handleSubmitForm(formId, modalId, submit_type) {
    $(formId).submit(function(event) {
        event.preventDefault();
        var customerId = $('#customerId').val();
        var payerId = $('#payerId').val();
        var addressId = $('#addressId').val();
        var deviceId = $('#deviceId').val();
        var orderId = $('#orderId').val();
        var base_redirect_url = '/orders/' + orderId + '/update/'
        var formData = $(this).serialize();
        formData += '&order_id=' + orderId;
        formData += '&customer=' + customerId;

        var url;
        if (submit_type === 'customer' || submit_type === 'payer') {
            url = '/orders/customer_create/';
        } else if (submit_type === 'address') {
            url = '/orders/address_create/';
        } else if (submit_type === 'device') {
            url = '/orders/device_create/';
        }

        $.ajax({
            type: 'POST',
            url: url,
            data: formData,
            success: function(response) {
                if (response.success) {

                    var redirect_url;
                    if (submit_type === 'customer') {
                        redirect_url = base_redirect_url + '?customer_id=' + response.customer_id + '&payer_id=' + payerId + '&address_id=' + addressId + '&device_id=' + deviceId;
                    } else if (submit_type === 'payer') {
                        redirect_url = base_redirect_url + '?customer_id=' + customerId + '&payer_id=' + response.customer_id + '&address_id=' + addressId + '&device_id=' + deviceId;
                    } else if (submit_type === 'address') {
                        redirect_url = base_redirect_url + '?customer_id=' + customerId + '&payer_id=' + payerId + '&address_id=' + response.address_id + '&device_id=' + deviceId;
                    } else if (submit_type === 'device') {
                        redirect_url = base_redirect_url + '?customer_id=' + customerId + '&payer_id=' + payerId + '&address_id=' + addressId + '&device_id=' + response.device_id;
                    }

                    $(modalId).modal('hide');
                    alert('Successfully Created!');
                    window.location.href = redirect_url;
                } else {
                    alert('An error occurred while adding.');
                }
            }
        });
    });
}

handleSubmitForm('#customerForm', '#addCustomerModal', 'customer');
handleSubmitForm('#payerForm', '#addPayerModal',  'payer');
handleSubmitForm('#addressForm', '#addAddressModal',  'address');
handleSubmitForm('#deviceForm', '#addDeviceModal',  'device');


document.addEventListener('DOMContentLoaded', function() {
    var serviceSelect = document.getElementById('id_service_services');

    function updateServiceOptions() {
        var brandId = document.getElementById('filterByBrand').value;
        var modelId = document.getElementById('filterByModel').value;

        $.ajax({
            url: '/orders/services_filter/',
            type: 'GET',
            data: {
                brand_id: brandId,
                model_id: modelId
            },
            success: function(response) {
                while (serviceSelect.firstChild) {
                    serviceSelect.removeChild(serviceSelect.firstChild);
                }

                response.forEach(function(service) {
                    var optionElement = document.createElement('option');
                    optionElement.value = service.id;
                    optionElement.textContent = service.name;
                    serviceSelect.appendChild(optionElement);
                });

                if (response.length > 0) {
                    var serviceId = response[0].id;
                    var serviceField = document.getElementById('id_service_services');

                    serviceField.value = serviceId;
                }
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
            }
        });
    }

    document.getElementById('filterByBrand').addEventListener('change', updateServiceOptions);
    document.getElementById('filterByModel').addEventListener('change', updateServiceOptions);

    updateServiceOptions();
});


function updateSummary() {
    var totalPrice = 0;

    $('#service-table-body tr').each(function() {
        var quantity = parseInt($(this).find('td:nth-child(3)').text());
        var price = parseFloat($(this).find('td:nth-child(4)').text());

        if (!isNaN(quantity) && !isNaN(price)) {
            totalPrice += quantity * price;
        }
    });

    $('#total_summary').text(totalPrice.toFixed(2));
}


$(document).ready(function() {
    $('#id_service_services').change(function() {
        var selectedServiceId = $(this).val();

        $.ajax({
            url: '/orders/service_details/' + selectedServiceId + '/',
            dataType: 'json',
            success: function(data) {
                $('#id_service_name').val(data.name);
                $('#id_service_price_net').val(data.price_net);
                $('#id_service_quantity').val(data.quantity);
            },
        });
    });
});


$(document).ready(function() {
    $('#serviceForm').submit(function(event) {
        event.preventDefault();

        var formData = $(this).serialize();
        var serviceId = $('#order_service_id').val();

        formData += '&order_service_id=' +  serviceId;

        $.ajax({
            url: $(this).attr('action'),
            type: $(this).attr('method'),
            data: formData,
            success: function(response) {
                $('#addServiceModal').modal('hide');

                var orderId = $('#orderId').val();

                updateServiceTable(orderId);

                $('#service_details-tab').tab('show');
            },
        });
    });
});


function updateServiceTable(orderId) {
    $.ajax({
        url: '/orders/services_list/',
        method: 'GET',
        data: {
            'order_id': orderId
        },
        dataType: 'json',
        success: function(data) {
            var tableBody = '';
            data.services.forEach(function(service) {
                tableBody += '<tr>';
                tableBody += '<td hidden="hidden">' + service.id + '</td>';
                tableBody += '<td>' + service.name + '</td>';
                tableBody += '<td>' + service.quantity + '</td>';
                tableBody += '<td>' + service.price_net + '</td>';
                tableBody += '<td>';
                tableBody += '<div class="btn-group me-2">';
                tableBody += '<button type="button" class="btn btn-sm btn-outline-secondary" id="service-edit">Update</button>';
                tableBody += '<button type="button" class="btn btn-sm btn-outline-secondary service-delete-btn" data-service-id="' + service.id + '">Delete</button>';
                tableBody += '</div>';
                tableBody += '</td>';
                tableBody += '</tr>';
            });
            tableBody += '<tr id="summary-row">';
            tableBody += '<td colspan="2"><b>Summary:</b></td>';
            tableBody += '<td id="total_summary" style="font-weight: bold;">{{ total_summary }}</td>';
            tableBody += '<td><b>NET PLN</b></td>';
            tableBody += '<td></td>';
            tableBody += '</tr>';
            $('#service-table-body').html(tableBody);
            updateSummary();

            $('.service-delete-btn').click(function() {
                var serviceIdToDelete = $(this).data('service-id');
                var orderId = $('#orderId').val();

                $.ajax({
                    url: '/orders/service_delete/',
                    type: 'POST',
                    data: {
                        'pk': serviceIdToDelete,
                        'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
                    },
                    dataType: 'json',
                    success: function(response) {
                        updateServiceTable(orderId);
                    },
                });
            });
        },
    });
}


$(document).ready(function() {
    $('#service-table-body').on('click', 'button#service-edit', function() {
        var serviceId = $(this).closest('tr').find('td:first-child').text();

        $.ajax({
            url: '/orders/service_update/',
            method: 'GET',
            data: {
                'service_id': serviceId
            },
            dataType: 'json',
            success: function(response) {
                $('#order_service_id').val(response.id);
                $('#id_service_services').val(response.service);
                $('#id_service_name').val(response.name);
                $('#id_service_price_net').val(response.price_net);
                $('#id_service_quantity').val(response.quantity);

                updateSummary();

                $('#addServiceModal').modal('show');

            },
        });
    });
});

updateSummary()


$(document).ready(function() {
    $('.service-delete-btn').click(function() {
        var serviceIdToDelete = $(this).closest('tr').find('td:first-child').text();
        var orderId = $('#orderId').val();

        $.ajax({
            url: '/orders/service_delete/',
            type: 'POST',
            data: {
                'pk': serviceIdToDelete,
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            dataType: 'json',
            success: function(response) {
                updateServiceTable(orderId);
            },
        });
    });
});


$(document).ready(function() {
    var container = document.querySelector("#attachment_form")
    var addButton = document.querySelector("#add_more")
    var totalForms = document.querySelector("#id_form-TOTAL_FORMS")
    var formNum = 0;

    addButton.addEventListener('click', addForm)

    function addForm(e) {
        e.preventDefault()
        let form = document.querySelector(".attachment_form");
        let newForm = form.cloneNode(true)
        let formRegex = RegExp(`form-(\\d){1}-`, 'g')
        formNum++

        newForm.innerHTML = newForm.innerHTML.replace(formRegex, `form-${formNum}-`)
        container.insertBefore(newForm, addButton)

        totalForms.setAttribute('value', `${formNum + 1}`)
    }
});


$(document).ready(function() {
  $(document).on('click', '.delete-button', function(event) {
    event.preventDefault();
    var attachmentId = $(this).data('attachment-id');
    var orderId = $('#orderId').val();
    var url = "/orders/attachment/" + attachmentId + "/delete/?order_id=" + orderId;

    fetch(url)
      .then(response => response.text())
      .then(data => {
        document.getElementById("attachment_list").innerHTML = data;
      })
      .catch(error => {
        console.error("Error:", error);
      });
  });
});


function checkFileSize(input) {
    const maxSize = 40 * 1024 * 1024;
    if (input.files && input.files[0]) {
        const fileSize = input.files[0].size;
        if (fileSize > maxSize) {
            document.getElementById("fileSizeError").style.display = "block";
            input.value = "";
        } else {
            document.getElementById("fileSizeError").style.display = "none";
        }
    }
}


function getReportt(orderId) {
alert('dsada')
    var detailsRow = document.getElementById('row' + orderId);
    detailsRow.classList.toggle('show');
}


function getReport(orderId){
    var endpointURL = "/orders/api/" + orderId + "/get_report/";

    var xhr = new XMLHttpRequest();
    xhr.open('GET', endpointURL, true);
    xhr.responseType = 'blob';

    xhr.onload = function() {
        if (xhr.status === 200) {
            var filename = xhr.getResponseHeader('Content-Disposition').split('filename=')[1];
            var blob = new Blob([xhr.response], { type: 'application/pdf' });
            var url = window.URL.createObjectURL(blob);
            var a = document.createElement('a');
            a.href = url;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
        }
    };

    xhr.send();
}


function sendReport(orderId) {
    var email = document.getElementById('emailInput').value;

    if (email.trim() === '') {
        alert('Please enter your email address.');
        return;
    }
    var endpointURL = "/orders/api/" + orderId + "/send_report/?email_to=" + encodeURIComponent(email);
    var xhr = new XMLHttpRequest();
    xhr.open('GET', endpointURL, true);
    xhr.send();
}


document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("reportForm").addEventListener("submit", function (event) {
        event.preventDefault();

        var orderId = document.getElementById("orderId").value;
        var email = document.getElementById("emailInput").value;

        sendReport(orderId, email);
    });
});

function sendReport(orderId, email) {
    var endpointURL = "/orders/api/" + orderId + "/send_report/?email_to=" + encodeURIComponent(email);
    $('#sendReportModal').modal('hide')
    var xhr = new XMLHttpRequest();
    xhr.open('GET', endpointURL, true);
    xhr.send();
}
