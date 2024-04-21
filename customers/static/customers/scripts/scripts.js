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

    function sendSearchRequest() {
        var searchQuery = searchInput.value.trim();

        // Assign null to previousSearchQuery if searchQuery is empty
        if (searchQuery === "") {
            previousSearchQuery = null;
        }

        var url = "/customers/?search=";

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
