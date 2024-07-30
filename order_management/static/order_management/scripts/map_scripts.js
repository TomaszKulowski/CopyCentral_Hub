var markers = L.markerClusterGroup({
    maxClusterRadius: 50,
    disableClusteringAtZoom: 17,
    spiderfyOnMaxZoom: true,
    showCoverageOnHover: false,
    zoomToBoundsOnClick: true,


});

document.addEventListener("DOMContentLoaded", function() {
    var mapElement = document.getElementById('map');
    var ordersData = mapElement.getAttribute('data-orders');

    var orders;
    try {
        orders = JSON.parse(ordersData);
    } catch (error) {
        console.error('Error parsing data-orders:', error);
        return;
    }

    var map = L.map('map').setView([51.505, -0.09], 11);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    var bounds = L.latLngBounds();

    for (var key in orders) {
        if (orders.hasOwnProperty(key)) {
            var order = orders[key];
            var selectedExecutorId = "selected_" + key;
            var selectedExecutorElement = document.getElementById(selectedExecutorId);

            if (selectedExecutorElement) {
                var color = selectedExecutorElement.getAttribute('data-color');
                if (color === 'None') {
                    color = '#e60000';
                }
            } else {
                var color = '#e60000';
            }

            var lat = order[0];
            var lng = order[1];
            var modal = "#orderModal_" + key;

            if (lat !== 'None' && lng !== 'None' && lat && lng) {
                (function(modal, color) {
                    var svgIcon = `
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" style="fill: ${color};" class="bi bi-geo-alt-fill" viewBox="0 0 16 16">
                          <path d="M8 16s6-5.686 6-10A6 6 0 0 0 2 6c0 4.314 6 10 6 10m0-7a3 3 0 1 1 0-6 3 3 0 0 1 0 6"/>
                        </svg>`;

                    var marker = L.divIcon({
                        className: 'custom-icon',
                        html: svgIcon,
                        iconSize: [50, 101],
                        iconAnchor: [25, 50],
                        popupAnchor: [0, -100]
                    });

                    var markerInstance = L.marker([parseFloat(lat), parseFloat(lng)], { icon: marker, orderId: key }).on('click', function(e) {
                        $(modal).modal('show');
                    });

                    markers.addLayer(markerInstance);
                    bounds.extend(markerInstance.getLatLng());
                })(modal, color);
            }
        }
    }

    map.addLayer(markers);

    if (bounds.isValid()) {
        map.fitBounds(bounds);
    }
});


function updateMarkerColor(orderId, color) {
    var marker = findMarkerByOrderId(orderId);

    if (marker) {
        var svgIcon = `
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" style="fill: ${color};" class="bi bi-geo-alt-fill" viewBox="0 0 16 16">
              <path d="M8 16s6-5.686 6-10A6 6 0 0 0 2 6c0 4.314 6 10 6 10m0-7a3 3 0 1 1 0-6 3 3 0 0 1 0 6"/>
            </svg>`;

        marker.setIcon(L.divIcon({
            className: 'custom-icon',
            html: svgIcon,
            iconSize: [50, 101],
            iconAnchor: [25, 50]
        }));

    } else {
        console.error(`Marker not found for order ID: ${orderId}`);
    }
}


function findMarkerByOrderId(orderId) {
    for (var i = 0; i < markers.getLayers().length; i++) {
        var layer = markers.getLayers()[i];
        if (layer.options.orderId.toString() === orderId.toString()) {
            return layer;
        }
    }
    return null;
}


$(document).ready(function() {
  $('.executor-select').change(function() {
    var selectedType = 'executor';
    var selectedValue = $(this).val();
    var selectedOption = $(this).find('option:selected');
    var color = selectedOption.data('color');
    var orderId = $(this).data('order-id');
    updateMarkerColor(orderId, color);

    var url = "/orders/api/" + orderId + "/order_update/";

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
