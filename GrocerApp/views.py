import json

from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.db.models import Q
from .forms import CategoryForm, ProductForm, ReviewForm, BlogForm, SignUpForm
from .models import Category, Product, Review, Blog, Cart, CartItem, Subscriber, Order
from .mpesa import lipa_na_mpesa_online
import logging
from django.core.paginator import Paginator
from django.contrib import messages
from django.urls import reverse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .send_sms_email import send_sms, send_email_notifications
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SMSSerializer



@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f"{product.name} has been added to your cart!")
    return redirect('cart')



def cart_view(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    total_quantity = sum(item.quantity for item in cart_items)

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'total_quantity': total_quantity,
    })

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        amount = request.POST.get('amount')
        payment_method = request.POST.get('payment_method')

        logger.debug(f"Phone Number: {phone_number}, Email: {email}, Amount: {amount}, Payment Method: {payment_method}")

        if not phone_number or not amount or not payment_method:
            return JsonResponse({'success': False, 'message': 'Invalid order details.'})

        try:
            total_amount = sum(item.product.price * item.quantity for item in cart_items)
            logger.debug(f"Total Amount Calculated: {total_amount}")

            if float(amount) != total_amount:
                return JsonResponse({'success': False, 'message': 'Amount mismatch.'})

            order = Order.objects.create(
                user=request.user,
                phone_number=phone_number,
                email=email,
                amount=total_amount,
                payment_method=payment_method
            )

            # Clear cart items
            cart_items.delete()

            logger.debug("Order created and cart items deleted.")
            return JsonResponse({'success': True, 'redirect_url': reverse('checkout_success')})
        except Exception as e:
            logger.error(f"Exception occurred: {e}")
            return JsonResponse({'success': False, 'message': str(e)})

    return render(request, 'checkout.html', {'cart_items': cart_items, 'total_price': total_price})



@login_required
def checkout_success(request):
    return render(request, 'checkout_success.html')



def signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'sign up.html', {'error_message': "Passwords do not match."})

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return render(request, 'sign up.html', {'error_message': "Email is already registered."})

        user = User.objects.create_user(username=email, email=email, password=password)
        user.save()
        messages.success(request, "Account created successfully. Please log in.")
        return redirect('signup_confirmation')
    return render(request, 'sign up.html')


def signup_confirmation(request):
    return render(request, 'signup_confirmation.html')

def index(request):
    category_form = CategoryForm()
    product_form = ProductForm()
    review_form = ReviewForm()
    blog_form = BlogForm()
    categories = Category.objects.all()
    products = Product.objects.all()
    reviews = Review.objects.all()
    blogs = Blog.objects.all()
    context = {
        'category_form': category_form,
        'product_form': product_form,
        'review_form': review_form,
        'blog_form': blog_form,
        'categories': categories,
        'products': products,
        'reviews': reviews,
        'blogs': blogs,
    }
    return render(request, 'index.html', context)

def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    return redirect('index')

def products(request):
    products_list = Product.objects.all()
    paginator = Paginator(products_list, 10)  # Show 10 products per page
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    return render(request, 'products.html', {'products': products})

def features(request):
    return render(request, 'features.html')

def categories(request):
    return render(request, 'categories.html')

def reviews(request):
    return render(request, 'reviews.html')

def blogs(request):
    return render(request, 'blogs.html')

@csrf_exempt
def subscribe(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email', '')
            validate_email(email)
            Subscriber.objects.create(email=email)
            return JsonResponse({'success': True, 'message': 'Successfully subscribed!'})
        except ValidationError:
            return JsonResponse({'success': False, 'message': 'Invalid email address. Please enter a valid email.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    return redirect('index')

def create_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    return redirect('index')

def create_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    return redirect('index')

def process_payment(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        amount = request.POST.get('amount')
        payment_method = request.POST.get('payment_method')

        if not phone_number or not amount or not payment_method:
            return JsonResponse({'success': False, 'message': 'Invalid payment details.'})

        try:
            if payment_method == 'mpesa':
                result = lipa_na_mpesa_online(phone_number, amount)
                if result['ResponseCode'] == '0':
                    return JsonResponse({'success': True, 'message': 'Payment processed successfully.'})
                else:
                    return JsonResponse({'success': False, 'message': 'Payment failed: ' + result.get('errorMessage', 'Unknown error')})
            else:
                return JsonResponse({'success': False, 'message': 'Unsupported payment method.'})
        except Exception as e:
            logger.error(f"Error processing payment: {e}")
            return JsonResponse({'success': False, 'message': 'An error occurred while processing the payment.'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})





def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # Redirect to the home page or any other page
        else:
            messages.error(request, "Invalid email or password.")
            return render(request, 'login.html', {'error_message': "Invalid email or password."})

    return render(request, 'login.html')

@login_required
@require_POST
def delete_cart_item(request, item_id):
    if request.method == 'POST':
        try:
            cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
            cart_item.delete()
            cart = Cart.objects.get(user=request.user)
            total_quantity = sum(item.quantity for item in CartItem.objects.filter(cart=cart))
            return JsonResponse({'success': True, 'total_quantity': total_quantity})
        except CartItem.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Item does not exist.'})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

@csrf_exempt
def search_item(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            query = data.get('query', '')
            if query:
                products = Product.objects.filter(name__icontains=query)
                results = [{'id': product.id, 'name': product.name, 'price': product.price, 'image': product.image.url if product.image else ''} for product in products]
                return JsonResponse({'success': True, 'results': results})
            return JsonResponse({'success': False, 'message': 'No query provided.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})




logger = logging.getLogger(__name__)


@csrf_exempt
@login_required
def place_order(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        amount = request.POST.get('amount')
        payment_method = request.POST.get('payment_method')

        logger.debug(
            f"Received order details: Phone={phone_number}, Email={email}, Amount={amount}, Payment Method={payment_method}")

        if not phone_number or not email or not amount or not payment_method:
            logger.error("Invalid order details provided.")
            return JsonResponse({'success': False, 'message': 'Invalid order details.'})

        try:
            cart = get_object_or_404(Cart, user=request.user)
            total_amount = sum(item.product.price * item.quantity for item in CartItem.objects.filter(cart=cart))
            logger.debug(f"Total amount calculated: {total_amount}")

            if float(amount) != total_amount:
                logger.error("Amount mismatch.")
                return JsonResponse({'success': False, 'message': 'Amount mismatch.'})

            order = Order.objects.create(
                user=request.user,
                phone_number=phone_number,
                email=email,
                amount=total_amount,
                payment_method=payment_method
            )

            # Delete cart items
            CartItem.objects.filter(cart=cart).delete()
            logger.info("Order created and cart items deleted.")

            return JsonResponse({'success': True, 'redirect_url': reverse('checkout_success')})
        except Exception as e:
            logger.error(f"Exception occurred: {e}")
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})


logger = logging.getLogger(__name__)

@csrf_exempt
def mpesa_payment(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        amount = request.POST.get('amount')
        response = lipa_na_mpesa_online(phone_number, amount)

        if response.get('ResponseCode') == '0':
            send_sms(phone_number, "Your payment was successful.")
            send_email_notifications(
                [{'phone_number': phone_number, 'email': request.user.email}],
                "Your payment was successful."
            )
            return redirect('payment_success')
        else:
            return render(request, 'mpesa_payment.html', {'error': 'Payment failed. Please try again.'})
    return render(request, 'mpesa_payment.html')


logger = logging.getLogger(__name__)

@csrf_exempt
def confirm_order(request, order_id):
    logger.info("Received order confirmation request")
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        order.confirmed = True
        order.save()
        logger.info("Order confirmed")

        # Prepare recipient data
        recipient = [{'phone_number': order.phone_number, 'email': order.email}]

        # Send confirmation email using the phone number as email
        send_email_notifications(recipient, "Your order has been confirmed. Thank you for shopping with us!")
        logger.info("Confirmation email sent")

        # Get carrier information from the form
        carrier = request.POST.get('carrier')

        # Send confirmation SMS
        send_sms(order.phone_number, "Your order has been confirmed. Thank you for shopping with us!", carrier)
        logger.info(f"SMS sent to {order.phone_number} via {carrier}")

        return JsonResponse({'success': True, 'message': 'Order confirmed and notification sent.', 'redirect_url': '/checkout/success/'})
    logger.error("Invalid request method")
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


class SendSMSView(APIView):
    def post(self, request):
        serializer = SMSSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            message = serializer.validated_data['message']
            carrier = serializer.validated_data['carrier']

            # Call the send_sms function
            send_sms(phone_number, message, carrier)
            logger.info(f"SMS sent to {phone_number} via {carrier}")

            return Response({'success': 'SMS sent successfully'}, status=status.HTTP_200_OK)
        logger.error("Invalid data provided")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
def logout_view(request):
    logout(request)
    return redirect('index')