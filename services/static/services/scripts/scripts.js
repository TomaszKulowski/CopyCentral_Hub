document.addEventListener("DOMContentLoaded", function () {
    var tables = document.querySelectorAll(".table-striped");
    tables.forEach(function(table) {
        table.addEventListener("click", function(event) {
            var target = event.target.closest("tr");
            if (target) {
                var urlCell = target.querySelector("td:first-child");
                if (urlCell) {
                    var url = urlCell.textContent;
                    window.location.href = url;
                }
            }
        });
    });
});


$(document).ready(function() {
    $('#selectModel').on('change', function() {
        var selectedModel = $(this).val();
        if(selectedModel === 'All') {
            $('.model-services').show(); // Show all sections
        } else {
            $('.model-services').hide(); // Hide all sections initially
            $('.' + selectedModel).show(); // Show the section corresponding to the selected model
        }
    });
});
