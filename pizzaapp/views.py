from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Category, Product, Order, OrderItem
from .utils import generate_pdf_receipt

# Головна сторінка
def index(request):
    categories = Category.objects.all()
    return render(request, 'pizzaapp/index.html', {'categories': categories})

# Список товарів у категорії
def category_products(request, cat_id):
    category = get_object_or_404(Category, id=cat_id)
    products = category.products.all()
    return render(request, 'pizzaapp/category.html', {'category': category, 'products': products})

# Деталі товару
def product_detail(request, prod_id):
    product = get_object_or_404(Product, id=prod_id)
    return render(request, 'pizzaapp/product_detail.html', {'product': product})

# Реєстрація
def user_register(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('index')
    return render(request, 'pizzaapp/register.html', {'form': form})

# Логін
def user_login(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('index')
    return render(request, 'pizzaapp/login.html', {'form': form})

# Логаут
def user_logout(request):
    logout(request)
    return redirect('index')

# Кошик (сесії)
def _get_cart(request):
    return request.session.setdefault('cart', {})

# Перегляд кошика
def view_cart(request):
    cart = _get_cart(request)
    items = []
    total = 0
    for prod_id_str, qty in cart.items():
        prod = get_object_or_404(Product, id=int(prod_id_str))
        subtotal = prod.price * qty
        items.append({'product': prod, 'quantity': qty, 'subtotal': subtotal})
        total += subtotal
    return render(request, 'pizzaapp/cart.html', {'items': items, 'total': total})

# Додати до кошика
def add_to_cart(request, prod_id):
    cart = _get_cart(request)
    key = str(prod_id)
    cart[key] = cart.get(key, 0) + 1
    request.session.modified = True
    return redirect('view_cart')

# Видалити з кошика
def remove_from_cart(request, prod_id):
    cart = _get_cart(request)
    cart.pop(str(prod_id), None)
    request.session.modified = True
    return redirect('view_cart')

# Оформлення замовлення
@login_required
def create_order(request):
    cart = _get_cart(request)
    if not cart:
        return redirect('view_cart')
    order = Order.objects.create(user=request.user)
    for prod_id_str, qty in cart.items():
        OrderItem.objects.create(order=order, product_id=int(prod_id_str), quantity=qty)
    request.session['cart'] = {}
    request.session.modified = True
    return redirect('order_receipt', order_id=order.id)

# PDF-квитанція
@login_required
def order_receipt(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return generate_pdf_receipt(order)

# Обране: список
@login_required
def view_favorites(request):
    products = request.user.favorite_products.all()
    return render(request, 'pizzaapp/favorites.html', {'products': products})

# Обране: додати
@login_required
def add_to_favorites(request, prod_id):
    product = get_object_or_404(Product, id=prod_id)
    request.user.favorite_products.add(product)
    return redirect('view_favorites')

# Обране: видалити
@login_required
def remove_from_favorites(request, prod_id):
    product = get_object_or_404(Product, id=prod_id)
    request.user.favorite_products.remove(product)
    return redirect('view_favorites')