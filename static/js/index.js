document.addEventListener('DOMContentLoaded', function() {
    // Filter Button
    const filterBtn = document.getElementById('filter-btn');
    const filterWindow = document.getElementById('filter-window');

    filterBtn.addEventListener('click', function() {
        if (filterWindow.style.display === 'block') {
            filterWindow.style.display = 'none';
        } else {
            filterWindow.style.display = 'block';
        }
    });

    // Sort Player Name by Alphabetic Order
    const sortIcon = document.getElementById('sort-icon');

    sortIcon.addEventListener('click', function() {
        // Get all the player data rows
        const playerDataRows = document.querySelectorAll('#player-data');

        // Convert the player data rows NodeList to an array for sorting
        const sortedRows = Array.from(playerDataRows).sort((a, b) => {
            const playerA = a.querySelector('#name-txt').textContent;
            const playerB = b.querySelector('#name-txt').textContent;
            return playerA.localeCompare(playerB);
        });

        // Clear the table body
        const tableBody = document.querySelector('tbody');
        tableBody.innerHTML = '';

        // Append the sorted player data rows back to the table body
        sortedRows.forEach(row => {
            tableBody.appendChild(row);
        });
    });
});

// Search Button
const searchInput = document.getElementById('search-input');

searchInput.addEventListener('keypress', function(event) {
  // Check if the pressed key is the Enter key (key code 13)
  if (event.keyCode === 13) {
    event.preventDefault(); // Prevent the default form submission
    document.getElementById('search-form').submit(); // Submit the form
  }
});

