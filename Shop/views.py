from django.http import JsonResponse
from django.shortcuts import render, redirect
import json
from .models import *
from .forms import CustomUserForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout


def home(request):
    products = Product.objects.filter(trending=True)
    return render(request, "index.html", {"products": products})


def products_index(request):
    products = Product.objects.filter(status=True)  # Fetch only active products
    return render(request, "Shop/products/index.html", {"products": products, "category_name": None})


def product_detail(request, product_id):
    try:
        product = Product.objects.get(id=product_id, status=True)
        return render(request, "Shop/products/detail.html", {"product": product})
    except Product.DoesNotExist:
        messages.warning(request, "Product not found")
        return redirect('products_index')


def register(request):
    print("Register view accessed")  # Debug statement
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Registration successful! Please login.")
            return redirect('login')  # Redirect to login page after successful registration
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserForm()
    
    return render(request, "register.html", {"form": form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {username}!")
            return redirect('home')  # Redirect to home page after successful login
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, "login.html")


def logout_view(request):
    """Logs out the user and redirects to the login page."""
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')

def categories(request):
    category = Category.objects.filter(status=1)
    return render(request, "categories.html", {"category": category})


def categoriesview(request, name):
    if (Category.objects.filter(name=name, status=1)):
        products = Product.objects.filter(category__name=name)
        return render(request, "Shop/products/index.html", {"products": products,"category_name": name})
    else:
        messages.warning(request, "No Such Category Found")

def product_details(request, cname, pname):
    if Category.objects.filter(name=cname, status=1).exists():
        if Product.objects.filter(category__name=cname, status=1).exists():
            product = Product.objects.filter(name=pname, status=1).first()
            if product:
                return render(request, "product_details.html", {"product": product})
            else:
                messages.error(request, "No Such Product Found")
                return redirect('categories')
        else:
            messages.error(request, "No Products Found in This Category")
            return redirect('categories')


def add_to_cart(request):
    # Handle both AJAX and regular form submissions
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    
    if request.user.is_authenticated:
        try:
            if is_ajax:
                # Handle AJAX request
                data = json.load(request)
                product_qty = int(data['product_qty'])
                product_id = int(data['pid'])
            else:
                # Handle regular form submission
                product_qty = 1  # Default quantity for form submissions
                product_id = int(request.POST.get('pid'))
            
            # Check if product exists
            try:
                product = Product.objects.get(id=product_id, status=True)
            except Product.DoesNotExist:
                if is_ajax:
                    return JsonResponse({'status': 'Product not found'}, status=404)
                else:
                    messages.error(request, "Product not found")
                    return redirect('products_index')
            
            # Check if quantity is valid
            if product_qty <= 0:
                if is_ajax:
                    return JsonResponse({'status': 'Invalid quantity'}, status=400)
                else:
                    messages.error(request, "Invalid quantity")
                    return redirect('product_detail', product_id=product_id)
            
            # Check if there's enough stock
            if product_qty > product.quantity:
                if is_ajax:
                    return JsonResponse({'status': f'Only {product.quantity} items available in stock'}, status=400)
                else:
                    messages.error(request, f"Only {product.quantity} items available in stock")
                    return redirect('product_detail', product_id=product_id)
            
            # Check if product is already in cart
            try:
                cart_item = Cart.objects.get(user=request.user, product=product)
                # Update quantity if item already exists
                cart_item.quantity += product_qty
                cart_item.save()
                if is_ajax:
                    return JsonResponse({'status': 'Cart updated successfully'}, status=200)
                else:
                    messages.success(request, "Cart updated successfully")
                    return redirect('cart')
            except Cart.DoesNotExist:
                # Create new cart item
                Cart.objects.create(
                    user=request.user,
                    product=product,
                    quantity=product_qty
                )
                if is_ajax:
                    return JsonResponse({'status': 'Product added to cart successfully'}, status=200)
                else:
                    messages.success(request, "Product added to cart successfully")
                    return redirect('cart')
                    
        except (KeyError, ValueError, json.JSONDecodeError) as e:
            if is_ajax:
                return JsonResponse({'status': 'Invalid request data'}, status=400)
            else:
                messages.error(request, "Invalid request data")
                return redirect('products_index')
        except Exception as e:
            if is_ajax:
                return JsonResponse({'status': f'Error: {str(e)}'}, status=500)
            else:
                messages.error(request, f"An error occurred: {str(e)}")
                return redirect('products_index')
    else:
        if is_ajax:
            return JsonResponse({'status': 'Login to Add Cart'}, status=401)
        else:
            messages.warning(request, "Please login to add items to cart")
            return redirect('login')


def wishlist_view(request):
    """View to display the wishlist"""
    if request.user.is_authenticated:
        wishlist_items = Wishlist.objects.filter(user=request.user)
        return render(request, "wishlist.html", {"wishlist_items": wishlist_items})
    else:
        messages.warning(request, "Please login to view your wishlist.")
        return redirect('login')


def cart(request):
    """View to display the shopping cart"""
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        total_price = sum(item.product.selling_price * item.quantity for item in cart_items)
        return render(request, "cart.html", {"cart_items": cart_items, "total_price": total_price})
    else:
        messages.warning(request, "Please login to view your cart.")
        return redirect('login')

def remove_from_cart(request, item_id):
    """View to remove an item from the cart"""
    if request.user.is_authenticated:
        try:
            cart_item = Cart.objects.get(id=item_id, user=request.user)
            cart_item.delete()
            messages.success(request, "Item removed from cart successfully.")
        except Cart.DoesNotExist:
            messages.error(request, "Item not found in cart.")
    else:
        messages.warning(request, "Please login to remove items from cart.")
    return redirect('cart')


def add_to_wishlist(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            try:
                data = json.load(request)
                product_id = int(data['pid'])
                
                # Check if product exists
                try:
                    product = Product.objects.get(id=product_id, status=True)
                except Product.DoesNotExist:
                    return JsonResponse({'status': 'Product not found'}, status=404)
                
                # Check if product is already in wishlist
                try:
                    wishlist_item = Wishlist.objects.get(user=request.user, product=product)
                    return JsonResponse({'status': 'Product already in wishlist'}, status=200)
                except Wishlist.DoesNotExist:
                    # Create new wishlist item
                    Wishlist.objects.create(
                        user=request.user,
                        product=product
                    )
                    return JsonResponse({'status': 'Product added to wishlist successfully'}, status=200)
                    
            except (KeyError, ValueError, json.JSONDecodeError) as e:
                return JsonResponse({'status': 'Invalid request data'}, status=400)
            except Exception as e:
                return JsonResponse({'status': f'Error: {str(e)}'}, status=500)
        else:
            return JsonResponse({'status': 'Login to Add to Wishlist'}, status=401)
    else:
        return JsonResponse({'status': 'Invalid Access'}, status=403)


def remove_from_wishlist(request, item_id):
    """View to remove an item from the wishlist"""
    if request.user.is_authenticated:
        try:
            wishlist_item = Wishlist.objects.get(id=item_id, user=request.user)
            wishlist_item.delete()
            messages.success(request, "Item removed from wishlist successfully.")
        except Wishlist.DoesNotExist:
            messages.error(request, "Item not found in wishlist.")
    else:
        messages.warning(request, "Please login to remove items from wishlist.")
    return redirect('wishlist')


def checkout(request):
    """View to display the checkout page"""
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        total_price = sum(item.product.selling_price * item.quantity for item in cart_items)
        
        if not cart_items:
            messages.warning(request, "Your cart is empty. Please add items to proceed to checkout.")
            return redirect('cart')
            
        return render(request, "checkout.html", {
            "cart_items": cart_items,
            "total_price": total_price
        })
    else:
        messages.warning(request, "Please login to proceed to checkout.")
        return redirect('login')


def place_order(request):
    """View to handle order placement"""
    if request.user.is_authenticated:
        if request.method == 'POST':
            try:
                cart_items = Cart.objects.filter(user=request.user)
                
                if not cart_items:
                    messages.error(request, "Your cart is empty. Please add items to place an order.")
                    return redirect('cart')
                
                # Validate form data
                full_name = request.POST.get('full_name')
                email = request.POST.get('email')
                address = request.POST.get('address')
                city = request.POST.get('city')
                postal_code = request.POST.get('postal_code')
                phone_number = request.POST.get('phone_number')
                payment_method = request.POST.get('payment_method')
                
                if not all([full_name, email, address, city, postal_code, phone_number, payment_method]):
                    messages.error(request, "Please fill in all required fields.")
                    return redirect('checkout')
                
                # Calculate total amount
                total_amount = sum(item.product.selling_price * item.quantity for item in cart_items)
                
                # Create order
                order = Order.objects.create(
                    user=request.user,
                    full_name=full_name,
                    email=email,
                    address=address,
                    city=city,
                    postal_code=postal_code,
                    total_amount=total_amount,
                    paid=(payment_method != 'cod')  # Mark as paid if not COD
                )
                
                # Create order items
                for cart_item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        product=cart_item.product,
                        quantity=cart_item.quantity,
                        price=cart_item.product.selling_price
                    )
                
                # Clear the cart
                cart_items.delete()
                
                messages.success(request, "Order placed successfully!")
                return redirect('order_confirmation', order_id=order.id)
                
            except Exception as e:
                messages.error(request, f"An error occurred while placing your order: {str(e)}")
                return redirect('checkout')
        else:
            return redirect('checkout')
    else:
        messages.warning(request, "Please login to place an order.")
        return redirect('login')


def order_confirmation(request, order_id):
    """View to display order confirmation"""
    if request.user.is_authenticated:
        try:
            order = Order.objects.get(id=order_id, user=request.user)
            return render(request, "order_confirmation.html", {"order": order})
        except Order.DoesNotExist:
            messages.error(request, "Order not found.")
            return redirect('home')
    else:
        messages.warning(request, "Please login to view order confirmation.")
        return redirect('login')

def about(request):
    """View to display the about page"""
    return render(request, "about.html")

def contact(request):
    """View to display the contact page"""
    return render(request, "contact.html")

    














