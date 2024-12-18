document.addEventListener('DOMContentLoaded', function () {
    const checkoutForm = document.getElementById('checkout-form');
    const loadingSpinner = document.getElementById('loading-spinner');

    // Toggle card payment fields based on selected payment method
    document.getElementById('payment-method').addEventListener('change', function() {
        const cardFields = document.getElementById('card-payment-fields');
        cardFields.style.display = this.value === 'card' ? 'block' : 'none';
    });

    // Handle form submission
    checkoutForm.addEventListener('submit', function (event) {
        event.preventDefault();
        loadingSpinner.style.display = 'block';

        const phoneNumber = document.getElementById('phone_number').value;
        const email = document.getElementById('email').value;
        const amount = document.getElementById('amount').value;
        const paymentMethod = document.getElementById('payment-method').value;
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        console.log('Form Data:', { phoneNumber, email, amount, paymentMethod, csrfToken });

        if (!phoneNumber || !email || !amount || !paymentMethod) {
            alert('Please fill in all the required fields.');
            loadingSpinner.style.display = 'none';
            return;
        }

        fetch(checkoutForm.action, {
            method: 'POST',
            body: new URLSearchParams({
                'phone_number': phoneNumber,
                'email': email,
                'amount': amount,
                'payment_method': paymentMethod,
                'csrfmiddlewaretoken': csrfToken
            }),
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        })
        .then(response => response.json())
        .then(data => {
            loadingSpinner.style.display = 'none';
            console.log('Response Data:', data);
            if (data.success) {
                alert('Order placed successfully!');
                window.location.href = data.redirect_url;
            } else {
                alert('Error: ' + data.message);
            }
        })
        .catch(error => {
            loadingSpinner.style.display = 'none';
            console.error('Error:', error);
            alert('Something went wrong. Please try again.');
        });
    });
});
