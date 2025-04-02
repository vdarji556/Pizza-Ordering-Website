from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from home.models import Pizza, Cart, CartItems  

def home(request):
    pizzas = Pizza.objects.all()
    return render(request, 'home.html', {'pizzas': pizzas})

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.warning(request, "Username does not exist.")
            return redirect('login')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, "Login successful!")
            return redirect('home')
        else:
            messages.error(request, "Invalid password. Please try again.")
            return redirect('login')
    
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        if not name or not username or not email or not phone or not password:
            messages.warning(request, "All fields are required.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.warning(request, "Username already exists.")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.warning(request, "Email is already in use.")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password, first_name=name)
        user.save()
        messages.success(request, "Account created successfully. Please log in.")
        return redirect('login')
    
    return render(request, 'register.html')

def cart(request):
    cart = Cart.objects.filter(is_paid=False, user=request.user).first()
    cart_items = cart.cartitems.all() if cart else []

    context = {
        'carts': cart,
        'cart_items': cart_items,
    }
    return render(request, 'cart.html', context)

def add_cart(request, pizza_uid):
    user = request.user
    pizza = get_object_or_404(Pizza, uid=pizza_uid)
    
    cart, _ = Cart.objects.get_or_create(user=user, is_paid=False)
    cart_item, created = CartItems.objects.get_or_create(cart=cart, pizza=pizza)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"Added {pizza.pizza_name} to cart! (Qty: {cart_item.quantity})")
    return redirect('home')

def remove_cart_items(request, cart_item_uid):
    try:
        CartItems.objects.get(uid=cart_item_uid).delete()
    except Exception as e:
        print(e)
    return redirect('cart')

def order(request):
    orders = Cart.objects.filter(is_paid=True, user=request.user)
    context = {'order': orders}
    return render(request, 'orders.html', context)

def increase_quantity(request, cart_item_uid):
    cart_item = get_object_or_404(CartItems, uid=cart_item_uid)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')

def decrease_quantity(request, cart_item_uid):
    cart_item = get_object_or_404(CartItems, uid=cart_item_uid)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')
