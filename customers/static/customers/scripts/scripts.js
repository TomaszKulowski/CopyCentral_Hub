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
            var url = "/customers/?search=";

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
