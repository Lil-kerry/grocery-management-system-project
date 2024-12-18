document.addEventListener('DOMContentLoaded', function () {
    const searchButton = document.getElementById('globalSearchButton');
    const searchInput = document.getElementById('search-box');
    const resultsContainer = document.getElementById('results-container');
    const modal = document.getElementById('search-results-modal');
    const closeModal = document.getElementsByClassName('close')[0];

    searchButton.addEventListener('click', function () {
        const query = searchInput.value.trim();
        if (query) {
            fetch('/search-item/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: JSON.stringify({ query: query })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                resultsContainer.innerHTML = '';  // Clear previous results
                if (data.success) {
                    if (data.results.length > 0) {
                        data.results.forEach(product => {
                            const productDiv = document.createElement('div');
                            productDiv.className = 'product';
                            productDiv.innerHTML = `
                                <h3>${product.name}</h3>
                                <p>Price: Ksh ${product.price}</p>
                                <img src="${product.image}" alt="${product.name}" width="100">
                                <a href="/add-to-cart/${product.id}/" class="btn">Add to Cart</a>
                            `;
                            resultsContainer.appendChild(productDiv);
                        });
                        modal.style.display = 'block';  // Show modal with results
                    } else {
                        resultsContainer.innerHTML = '<p>No products found.</p>';
                        modal.style.display = 'block';  // Show modal with no results
                    }
                } else {
                    resultsContainer.innerHTML = `<p>${data.message}</p>`;
                    modal.style.display = 'block';  // Show modal with error message
                }
            })
            .catch(error => {
                console.error('Error:', error);
                resultsContainer.innerHTML = '<p>An error occurred while fetching results.</p>';
                modal.style.display = 'block';  // Show modal with error message
            });
        } else {
            alert('Please enter a search query!');
        }
    });

    closeModal.onclick = function () {
        modal.style.display = 'none';
    }

    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    }
});
