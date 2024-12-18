document.addEventListener('DOMContentLoaded', function () {
    const deleteButtons = document.querySelectorAll('.delete-btn');
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    deleteButtons.forEach(button => {
        button.addEventListener('click', function (event) {
            event.preventDefault();
            const itemId = this.dataset.itemId;
            const url = `/delete-cart-item/${itemId}/`;

            fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json',
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const row = document.querySelector(`tr[data-item-id="${itemId}"]`);
                    row.remove();
                    alert('Item deleted successfully!');
                    // Update the total items count
                    document.getElementById('cart-count').textContent = data.total_items;
                } else {
                    alert('An error occurred. Please try again.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while deleting the item.');
            });
        });
    });

    // Update quantity
    const quantityInputs = document.querySelectorAll('.quantity-input');
    quantityInputs.forEach(input => {
        input.addEventListener('change', () => {
            const itemId = input.dataset.itemId;
            const newQuantity = input.value;

            fetch(`/cart/update/${itemId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ quantity: newQuantity }),
            }).then(response => location.reload());
        });
    });

    // Search functionality
    const searchForm = document.querySelector('.search-form');
    const searchBox = document.querySelector('#search-box');

    searchForm.addEventListener('submit', function (event) {
        event.preventDefault();
        const query = searchBox.value;
        const url = `/search_item/`;

        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: query }),
        })
        .then(response => response.json())
        .then(data => {
            const resultsContainer = document.getElementById('search-results');
            resultsContainer.innerHTML = ''; // Clear previous results

            let totalPrice = 0;

            if (data.success && data.results.length > 0) {
                data.results.forEach(result => {
                    const resultCard = document.createElement('div');
                    resultCard.className = 'result-card';

                    const imgContainer = document.createElement('div');
                    imgContainer.className = 'img-container';
                    const img = document.createElement('img');
                    img.src = result.image;
                    img.alt = result.name;
                    imgContainer.appendChild(img);

                    const title = document.createElement('h3');
                    title.textContent = result.name;

                    const price = document.createElement('p');
                    price.textContent = `Price: Ksh. ${result.price}`;
                    totalPrice += parseFloat(result.price);

                    const rating = document.createElement('div');
                    rating.className = 'stars';
                    rating.innerHTML = `
                        <i class="fas fa-star"></i>
                        <i class="fas fa-star"></i>
                        <i class="fas fa-star"></i>
                        <i class="fas fa-star"></i>
                        <i class="fas fa-star-half-alt"></i>
                    `;

                    const addToCartButton = document.createElement('a');
                    addToCartButton.href = `/add_to_cart/${result.id}/`;
                    addToCartButton.className = 'btn';
                    addToCartButton.textContent = 'Add To Cart';

                    resultCard.appendChild(imgContainer);
                    resultCard.appendChild(title);
                    resultCard.appendChild(price);
                    resultCard.appendChild(rating);
                    resultCard.appendChild(addToCartButton);
                    resultsContainer.appendChild(resultCard);
                });

                const totalContainer = document.getElementById('total-container');
                totalContainer.innerHTML = `Total Price: Ksh. ${totalPrice.toFixed(2)}`;
            } else {
                resultsContainer.innerHTML = '<p>No results found.</p>';
            }
        })
        .catch(error => console.error('Error:', error));
    });
});
