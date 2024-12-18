from . import views
from django.urls import path
from .views import (
    add_to_cart, cart_view, checkout, checkout_success, signup, signup_confirmation,
    index, create_category, products, features, categories, reviews, blogs,
    subscribe, create_product, create_review, create_blog, process_payment,
    login_view, mpesa_payment, place_order, delete_cart_item, search_item, confirm_order, SendSMSView
)



urlpatterns = [
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart_view, name='cart'),
    path('checkout/', checkout, name='checkout'),
    path('checkout-success/', checkout_success, name='checkout_success'),
    path('signup/', signup, name='signup'),
    path('signup-confirmation/', signup_confirmation, name='signup_confirmation'),
    path('', index, name='index'),
    path('create-category/', create_category, name='create_category'),
    path('products/', products, name='products'),
    path('features/', features, name='features'),
    path('categories/', categories, name='categories'),
    path('reviews/', reviews, name='reviews'),
    path('blogs/', blogs, name='blogs'),
    path('subscribe/', subscribe, name='subscribe'),
    path('create-product/', create_product, name='create_product'),
    path('create-review/', create_review, name='create_review'),
    path('create-blog/', create_blog, name='create_blog'),
    path('process-payment/', process_payment, name='process_payment'),
    path('login/', login_view, name='login_view'),
    path('mpesa-payment/', mpesa_payment, name='mpesa_payment'),
    path('place-order/', place_order, name='place_order'),
    path('delete-cart-item/<int:item_id>/', delete_cart_item, name='delete_cart_item'),
    path('search-item/', search_item, name='search_item'),
    path('confirm-order/<int:order_id>/', confirm_order, name='confirm_order'),
    path('send-sms/', SendSMSView.as_view(), name='send_sms'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),

]







