document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.getElementById('search-form');
    const searchInput = document.getElementById('search');
    const demoOutput = document.getElementById('demo');

    searchForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the form from submitting
        demoOutput.innerHTML = searchInput.value; // Update the #demo element with the search input value
    });
});
