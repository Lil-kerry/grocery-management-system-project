let searchform = document.querySelector('.search-form');

document.querySelector('#search-btn').onclick = ()   =>{
    searchform.classList.toggle('active');
    shoppingcart.classList.remove('active');
    loginform.classList.remove('active');
    navbar.classList.remove('active');
}

let shoppingcart = document.querySelector('.shopping-cart');

document.querySelector('#cart-btn').onclick = ()   =>{
    shoppingcart.classList.toggle('active');
    searchform.classList.remove('active');
    loginform.classList.remove('active');
    navbar.classList.remove('active');
}

let loginform = document.querySelector('.login-form');

document.querySelector('#login-btn').onclick = ()   =>{
    loginform.classList.toggle('active');
    searchform.classList.remove('active');
    shoppingcart.classList.remove('active');
    navbar.classList.remove('active');
}

let navbar = document.querySelector('.navbar');

document.querySelector('#menu-btn').onclick = ()   =>{
    navbar.classList.toggle('active');
    searchform.classList.remove('active');
    shoppingcart.classList.remove('active');
    loginform.classList.remove('active');
}

window.onscroll = ()   =>{
    searchform.classList.remove('active');
    shoppingcart.classList.remove('active');
    loginform.classList.remove('active');
    navbar.classList.remove('active');
}

var swiper = new Swiper(".product-slider", {
    loop:true,
    spaceBetween: 20,
    autoplay: {
        delay: 7500,
        disableOnInteraction: false,
    },
    centeredSlides: true,
    breakpoints: {
      0: {
        slidesPerView: 1,
      },
      768: {
        slidesPerView: 2,
      },
      1024: {
        slidesPerView: 3,
      },
    },
  });

  var swiper = new Swiper(".review-slider", {
    loop:true,
    spaceBetween: 20,
    autoplay: {
        delay: 7500,
        disableOnInteraction: false,
    },
    centeredSlides: true,
    breakpoints: {
      0: {
        slidesPerView: 1,
      },
      768: {
        slidesPerView: 2,
      },
      1024: {
        slidesPerView: 3,
      },
    },
  });

document.addEventListener('DOMContentLoaded', function () {
    const subscribeForm = document.getElementById('subscribe-form');

    subscribeForm.addEventListener('submit', function (event) {
        event.preventDefault();

        const emailInput = document.querySelector('input[name="email"]');
        const email = emailInput.value;

        if (!email) {
            alert('Please enter a valid email address.');
            return;
        }

        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        fetch("{% url 'subscribe' %}", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken  // Include CSRF token in headers
            },
            body: JSON.stringify({ email: email })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Successfully subscribed!');
            } else {
                alert('Error: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Something went wrong. Please try again.');
        });

    });
});

document.addEventListener('DOMContentLoaded', function () {
    const subscribeForm = document.getElementById('subscribe-form');
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    subscribeForm.addEventListener('submit', function (event) {
        event.preventDefault();
        const email = subscribeForm.querySelector('input[name="email"]').value;
        const url = '/subscribe/';

        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email: email }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);
                subscribeForm.reset();
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Something went wrong. Please try again.');
        });
    });
});
