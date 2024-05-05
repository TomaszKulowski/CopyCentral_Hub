document.addEventListener("DOMContentLoaded", function () {
    var tableBody = document.getElementById("table-body");
    if (tableBody) {
        tableBody.addEventListener("click", function(event) {
            var target = event.target.closest("tr");
            if (target) {
                var urlElement = target.querySelector("td:first-child a");
                if (urlElement) {
                    var url = urlElement.getAttribute("href");
                    window.location.href = url;
                }
            }
        });
    }

    var searchInput = document.querySelector(".sea");
    var typingTimer;
    var previousSearchQuery = "";

    searchInput.addEventListener("input", function () {
        clearTimeout(typingTimer);
        typingTimer = setTimeout(function () {
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

        // Assign null to previousSearchQuery if searchQuery is empty
        if (searchQuery === "") {
            previousSearchQuery = null;
        }

        var url = "/orders/?search=";

        // Append the search parameter only if the searchQuery is not empty
        if (searchQuery !== "") {
            url += encodeURIComponent(searchQuery);
        }

        fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.text();
            })
            .then(data => {
                document.getElementById("table-body").innerHTML = data;
                document.getElementById("paginator").innerHTML = '';

                // Update the previous searchQuery only if searchQuery is not empty
                if (searchQuery !== "") {
                    previousSearchQuery = searchQuery;
                }
            })
            .catch(error => {
                console.error("Error:", error);
            });
    }
});


function loadCustomerDetails(customerId, orderId) {
    var customerDetailsUrl = "/orders/customer_details/" + customerId + "/";
    var addressFormUrl = "/orders/address_form/" + customerId + "/?order_id=" + orderId;

    fetch(customerDetailsUrl)
        .then(response => response.text())
        .then(data => {
            document.getElementById("customer-details").innerHTML = data;
        })
        .catch(error => {
            console.error("Error:", error);
        });

    fetch(addressFormUrl)
        .then(response => response.text())
        .then(data => {
            var inputs = document.querySelectorAll('#address-details input, #address-details textarea');
            inputs.forEach(function(input) {
                input.value = '';
            });
            document.getElementById("additional_address-select").innerHTML = data;
        })
        .catch(error => {
            console.error("Error:", error);
        });
   $('#customer-select').val(customerId).trigger('change');

}

$(document).ready(function() {
    $('#id_customer').on('select2:select', function (e) {
        var orderId = $('#orderId').val();
        var customerId = e.params.data.id;
        loadCustomerDetails(customerId, orderId);
    });
});


function loadPayerDetails(customerId) {
    var url = "/orders/customer_details/" + customerId + "/";

    fetch(url)
        .then(response => response.text())
        .then(data => {
            document.getElementById("payer-details").innerHTML = data;
        })
        .catch(error => {
            console.error("Error:", error);
        });
}

$(document).ready(function() {
    $('#id_payer').on('select2:select', function (e) {
        var customerId = e.params.data.id;
        loadPayerDetails(customerId);
    });
});


function loadAddressDetails(addressId) {
    var url = "/orders/address_details/" + addressId + "/";

    fetch(url)
        .then(response => response.text())
        .then(data => {
            document.getElementById("address-details").innerHTML = data;
        })
        .catch(error => {
            console.error("Error:", error);
        });
}

function clearAddressInputs() {
    var inputs = document.querySelectorAll('#address-details input, #address-details textarea');
    inputs.forEach(function(input) {
        input.value = '';
    });
}

$(document).ready(function() {
    $('#id_address').on('select2:select', function (e) {
        var addressId = e.params.data.id;
        loadAddressDetails(addressId);
    }).on('select2:unselect', function (e) {
        clearAddressInputs();
    });
});


function handleSubmitForm(formId, modalId, submit_type) {
    $(formId).submit(function(event) {

        event.preventDefault();
        var customerId = $('#customer-select').val() !== 'undefined' ? $('#customer-select').val() : '';
        var payerId = $('#payer-select').val() !== 'undefined' ? $('#payer-select').val() : '';
        var addressId = $('#additional_address-select').val() !== 'undefined' ? $('#additional_address-select').val() : '';
        var deviceId = $('#device-select').val() !== 'undefined' ? $('#device-select').val() : '';
        var orderId = $('#orderId').val();
        var base_redirect_url = orderId ? '/orders/' + orderId + '/update/' : '/orders/create/';
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
                if (response.status === 201) {
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
                    var errorsElement = document.getElementById("errors");
                    errorsElement.innerHTML = response.errors;
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


// order service filters
document.addEventListener('DOMContentLoaded', function() {
    var serviceSelect = document.getElementById('id_service_services');

    function updateServiceOptions() {
        var brandId = document.getElementById('filterByBrand').value;
        var modelId = document.getElementById('filterByModel').value;

        $.ajax({
            url: '/orders/api/services_filter/',
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


// when service select is changed get and fill received data order service field
$(document).ready(function() {
    $('#id_service_services').change(function() {
        var selectedServiceId = $(this).val();

        $.ajax({
            url: '/orders/api/service_details/' + selectedServiceId + '/',
            dataType: 'json',
            success: function(data) {
                $('#id_service_name').val(data.name);
                $('#id_service_price_net').val(data.price_net);
                $('#id_service_quantity').val(data.quantity);
            },
        });
    });
});


// update order service table
function updateServiceTable(orderId) {
    var url = "/orders/api/order_services_list/?order_id=" + orderId;

    fetch(url)
        .then(response => response.text())
        .then(data => {
            document.getElementById("service-table-body").innerHTML = data;
        })
        .catch(error => {
            console.error("Error:", error);
        });
}


// create/update order service
function orderServiceUpdate() {
    var orderId = $('#orderId').val();
    var formData = $('#serviceForm').serialize();
    var update = $('#OrderServiceUpdate').val();
    var orderServiceId = $('#order_service_id').val();
    var url = '';

    if (update === 'True') {
        url = "/orders/api/order_service_update/" + orderServiceId + "/";
    } else {
        url = '/orders/api/order_service_create/';
    }

    $.ajax({
        url: url,
        type: 'POST',
        data: formData,
        success: function(response) {
            updateServiceTable(orderId);
        },
        error: function(xhr, status, error) {
            console.error(xhr.responseText);
        },
        complete: function() {
            $('#addServiceModal').modal('hide');
            $('#OrderServiceUpdate').val('False');
        }
    });
}


// display edit order service form
$(document).ready(function() {
    $('#service-table-body').on('click', 'button#service-edit', function() {
        var serviceId = $(this).closest('tr').find('td:first-child').text();
        var fromSession = $(this).closest('tr').find('td:nth-child(2)').text();

        $.ajax({
            url: "/orders/api/order_service_details/" + serviceId + "/",
            method: 'GET',
            data: {
                'service_id': serviceId,
                'from_session': fromSession,
            },
            dataType: 'json',
            success: function(response) {
                $('#order_service_id').val(serviceId);
                $('#id_service_services').val(response.service);
                $('#id_service_name').val(response.name);
                $('#id_service_price_net').val(response.price_net);
                $('#id_service_quantity').val(response.quantity);
                $('#id_service_from_session').val(response.from_session);
                $('#OrderServiceUpdate').val('True');
                $('#addServiceModal').modal('show');

            },
        });
    });
});


// delete order service
$(document).ready(function() {
    $(document).on('click', '.service-delete-btn', function() {
        var serviceIdToDelete = $(this).closest('tr').find('td:first-child').text();
        var from_session = $(this).closest('tr').find('td:nth-child(2)').text();
        var orderId = $('#orderId').val();

        $.ajax({
            url: '/orders/api/order_service_delete/',
            type: 'POST',
            data: {
                'pk': serviceIdToDelete,
                'order_from_session': from_session,
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
    $('#sendReportModal').modal('hide');
    var xhr = new XMLHttpRequest();
    xhr.open('GET', endpointURL, true);
    xhr.send();
}
