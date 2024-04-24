document.addEventListener("DOMContentLoaded", function() {
    document.addEventListener('click', function(event) {
        var target = event.target;
        if (target && target.classList.contains("btn-outline-secondary")) {
            var currentUrl = window.location.href;
            var forReviewValue = getParameterByName('for_review', currentUrl);

            var orderId = target.getAttribute('data-order-id');
            var action = target.getAttribute('data-action');
            updateReview(orderId, action, forReviewValue);
        }
    });

    function getParameterByName(name, url) {
        if (!url) url = window.location.href;
        name = name.replace(/[\[\]]/g, "\\$&");
        var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
            results = regex.exec(url);
        if (!results) return null;
        if (!results[2]) return '';
        return decodeURIComponent(results[2].replace(/\+/g, " "));
    }

    function updateReview(orderId, actionType, forReview) {
        var url = "/order_review/";
        if (forReview === 'true') {
            url += "?for_review=true";
        }
        var csrftoken = getCookie('csrftoken');
        var data = {
            order_id: orderId,
            action_type: actionType,
            for_review: forReview,
            csrfmiddlewaretoken: csrftoken
        };

        $.ajax({
            url: url,
            type: 'POST',
            data: data,
            error: function(xhr, textStatus, errorThrown) {
                console.error("Error:", errorThrown);
            }
        })
        .done(function(response) {
            console.log('Success:', response);
            var reviewTableBody = document.getElementById("review-table-body");
            if (reviewTableBody) {
                reviewTableBody.innerHTML = response;
            } else {
                console.error("Element with ID 'review-table-body' not found.");
            }
        })
        .fail(function(error) {
            console.error("Error:", error);
        });
    }

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
});
