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
            var url = "/service_orders/?search=";


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

        window.location.href = '/service_orders/' + orderId + '/update/?customer_id=' + customerId + '&payer_id=' + payerId + '&address_id=' + addressId;
    });
});

$(document).ready(function() {
    $('#id_payer').on('select2:select', function (e) {
        var payerId = e.params.data.id;
        var orderId = $('#orderId').val();
        var customerId = $('#customerId').val();
        var addressId = $('#addressId').val();

        window.location.href = '/service_orders/' + orderId + '/update/?customer_id=' + customerId + '&payer_id=' + payerId + '&address_id=' + addressId;
    });
});

$(document).ready(function() {
    $('#id_address').on('select2:select', function (e) {
        var addressId = e.params.data.id;
        var orderId = $('#orderId').val();
        var customerId = $('#customerId').val();
        var payerId = $('#payerId').val();

        window.location.href = '/service_orders/' + orderId + '/update/?customer_id=' + customerId + '&payer_id=' + payerId + '&address_id=' + addressId;
    }).on('select2:unselect', function (e) {
        var addressId = null;
        var orderId = $('#orderId').val();
        var customerId = $('#customerId').val();
        var payerId = $('#payerId').val();

        window.location.href = '/service_orders/' + orderId + '/update/?customer_id=' + customerId + '&payer_id=' + payerId + '&address_id=' + addressId;
    });
});


function handleSubmitForm(formId, submit_type) {
    $(formId).submit(function(event) {
        event.preventDefault();
        var customerId = $('#customerId').val();
        var payerId = $('#payerId').val();
        var addressId = $('#addressId').val();
        var orderId = $('#orderId').val();
        var base_redirect_url = '/service_orders/' + orderId + '/update/'
        var formData = $(this).serialize();
        formData += '&order_id=' + orderId;
        formData += '&customer=' + customerId;

        var url;
        if (submit_type === 'customer' || submit_type === 'payer') {
            url = '/service_orders/customer_create/';
        } else if (submit_type === 'address') {
            url = '/service_orders/address_create/';
        }

        $.ajax({
            type: 'POST',
            url: url,
            data: formData,
            success: function(response) {
                if (response.success) {

                var redirect_url;
                if (submit_type === 'customer') {
                    redirect_url = base_redirect_url + '?customer_id=' + response.customer_id + '&payer_id=' + payerId + '&address_id=' + addressId;
                } else if (submit_type === 'payer') {
                    redirect_url = base_redirect_url + '?customer_id=' + customerId + '&payer_id=' + response.customer_id + '&address_id=' + addressId;
                } else if (submit_type === 'address') {
                    redirect_url = base_redirect_url + '?customer_id=' + customerId + '&payer_id=' + payerId + '&address_id=' + response.address_id;
                }

                    $(formId + 'Modal').modal('hide');
                    alert('Successfully Created!');
                    window.location.href = redirect_url;
                } else {
                    alert('An error occurred while adding.');
                }
            }
        });
    });
}

handleSubmitForm('#customerForm', 'customer');

handleSubmitForm('#payerForm', 'payer');

handleSubmitForm('#addressForm', 'address');
