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


// create customer
function customerCreate(customerType) {
    var url = '/orders/customer_create/';

    if (customerType === 'customer') {
        var formData = $('#customerForm').serialize();
        var my_field = document.getElementById('customer-select');

    } else if (customerType === 'payer') {
        var formData = $('#payerForm').serialize();
        var my_field = document.getElementById('payer-select');

    }

    $.ajax({
        url: url,
        type: 'POST',
        data: formData,
        error: function(xhr, status, error) {
            console.error(xhr.responseText);
        },
        success: function(response) {
            var new_option = document.createElement('option');
            new_option.text = response.customer_name;
            new_option.value = response.customer_id;

            my_field.appendChild(new_option);
            $(my_field).val(new_option.value).trigger('change');

            loadCustomerDetails(new_option.value, customerType);
            if ( customerType === 'customer') {
                clearAddressInputs();
            }
        },

        complete: function() {
            $('#addCustomerModal').modal('hide');
            $('#addPayerModal').modal('hide');
        }
    });
}


// create additional address
function addressCreate() {
    var url = '/orders/api/address_create/';
    var customerId = document.getElementById('customer-select').value;
    var formData = $('#addressForm').serialize();
    formData += '&customer=' + encodeURIComponent(customerId);

    $.ajax({
        url: url,
        type: 'POST',
        data: formData,
        error: function(xhr, status, error) {
            console.error(xhr.responseText);
        },
        success: function(response) {
        if (response.status === 400) {
            var div = document.getElementById('address_error');
            div.textContent = response.message;
        } else if (response.status === 201) {
            var my_field = document.getElementById('additional_address-select');
            var new_option = document.createElement('option');
            new_option.text = response.address_name;
            new_option.value = response.address_id;

            my_field.appendChild(new_option);
            $(my_field).val(new_option.value).trigger('change');

            loadAddressDetails(response.address_id)
        }

        },
        complete: function() {
            $('#addAddressModal').modal('hide');
        }
    });
}


// create device
function deviceCreate() {
    var url = '/orders/api/device_create/';
    var formData = $('#deviceForm').serialize();
    var errorDiv = $('#errors');

    $.ajax({
        url: url,
        type: 'POST',
        data: formData,
        dataType: 'json',
        error: function(xhr, status, error) {
            console.error(xhr.responseText);
        },
        success: function(response) {
            errorDiv.html('');

            if (response.status === 201) {
                var my_field = document.getElementById('device-select');
                var new_option = document.createElement('option');
                new_option.text = response.device_name;
                new_option.value = response.device_id;

                my_field.appendChild(new_option);
                $(my_field).val(new_option.value).trigger('change');
                $('#addDeviceModal').modal('hide');
            } else if (response.status === 400) {
                var errors = response.errors;
                var errorList = '';
                for (var field in errors) {
                    if (errors.hasOwnProperty(field)) {
                        errorList += errors[field];
                    }
                }
                errorDiv.html(errorList);
            }
        }
    });
}


// on customer select
$(document).ready(function() {
    $('#id_customer').on('select2:select', function (e) {
        var orderId = $('#orderId').val();
        var customerId = e.params.data.id;
        loadCustomerDetails(customerId, orderId);
        clearAddressInputs();
    });
});


// on payer select
$(document).ready(function() {
    $('#id_payer').on('select2:select', function (e) {
        var customerId = e.params.data.id;
        loadPayerDetails(customerId);
    });
});


// on address select
$(document).ready(function() {
    $('#id_address').on('select2:select', function (e) {
        var addressId = e.params.data.id;
        loadAddressDetails(addressId);
    }).on('select2:unselect', function (e) {
        clearAddressInputs();
    });
});



// load and fill customer details
function loadCustomerDetails(customerId, customerType) {
    var customerDetailsUrl = "/orders/api/customer_details/" + customerId + "/";

    fetch(customerDetailsUrl)
        .then(response => response.text())
        .then(data => {
           if (customerType === 'payer') {
               document.getElementById("payer-details").innerHTML = data;
           } else {
                document.getElementById("customer-details").innerHTML = data;
           }
        })
        .catch(error => {
            console.error("Error:", error);
        });
}


// load and fill payer details
function loadPayerDetails(customerId) {
    var url = "/orders/api/customer_details/" + customerId + "/";

    fetch(url)
        .then(response => response.text())
        .then(data => {
            document.getElementById("payer-details").innerHTML = data;
        })
        .catch(error => {
            console.error("Error:", error);
        });
}


// load and fill address details
function loadAddressDetails(addressId) {
    var url = "/orders/api/address_details/" + addressId + "/";

    fetch(url)
        .then(response => response.text())
        .then(data => {
            document.getElementById("address-details").innerHTML = data;
        })
        .catch(error => {
            console.error("Error:", error);
        });
}


// clear address inputs
function clearAddressInputs() {
    var div = document.getElementById('address_error');
    div.textContent = '';
    var inputs = document.querySelectorAll('#address-details input, #address-details textarea');
    inputs.forEach(function(input) {
        input.value = '';
    });
    $('#additional_address-select').val(null).trigger('change');
}


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


// add new attachment forms
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


// on delete attachment button
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


// check attachment file size
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


// get order report file
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


// send order report file
document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("reportForm").addEventListener("submit", function (event) {
        event.preventDefault();

        var orderId = document.getElementById("orderId").value;
        var email = document.getElementById("emailInput").value;

        sendReport(orderId, email);
    });
});

// send order report file
function sendReport(orderId, email) {
    var endpointURL = "/orders/api/" + orderId + "/send_report/?email_to=" + encodeURIComponent(email);
    $('#sendReportModal').modal('hide');
    var xhr = new XMLHttpRequest();
    xhr.open('GET', endpointURL, true);
    xhr.send();
}


// auto calculate total counter in the order template
document.addEventListener('DOMContentLoaded', function() {
    var monoCounter = document.getElementById('mono_counter');
    var colorCounter = document.getElementById('color_counter');
    var totalCounter = document.getElementById('total_counter');

    function updateTotalCounter() {
        var monoValue = parseInt(monoCounter.value) || 0;
        var colorValue = parseInt(colorCounter.value) || 0;
        totalCounter.value = monoValue + colorValue;
    }

    monoCounter.addEventListener('input', updateTotalCounter);
    colorCounter.addEventListener('input', updateTotalCounter);

    updateTotalCounter();
});

// auto calculate total counter in the device modal
document.addEventListener('DOMContentLoaded', function() {
    var monoCounter_device = document.getElementById('mono_counter_device');
    var colorCounter_device = document.getElementById('color_counter_device');
    var totalCounter_device = document.getElementById('total_counter_device');

    function updateTotalCounter() {
        var monoValue_device = parseInt(monoCounter_device.value) || 0;
        var colorValue_device = parseInt(colorCounter_device.value) || 0;
        totalCounter_device.value = monoValue_device + colorValue_device;
    }

    monoCounter_device.addEventListener('input', updateTotalCounter);
    colorCounter_device.addEventListener('input', updateTotalCounter);

    updateTotalCounter();
});


function toggleDetails(orderId) {
    var detailsRow = document.getElementById('row' + orderId);
    detailsRow.classList.toggle('show');
}