from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from store.models import Product
from .models import Cart, CartItem
from decimal import Decimal

def _cart_id(request):
    
    cart_id = request.session.session_key
    
    if not cart_id:
        cart_id = request.session.create()
    return cart_id

def add_cart(request,product_id):
    product = Product.objects.get(id = product_id)

    try:
        cart = Cart.objects.get(
            cart_id = _cart_id(request)
            )
        
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )

    try:
        cart_item= CartItem.objects.get(product=product, cart = cart)
        cart_item.quantity +=1
        cart_item.save()

    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart
        )

    return redirect("cart")

def minus_cart_item(request,product_id):
    product = get_object_or_404(Product, id= product_id)
    cart = Cart.objects.get(
        cart_id = _cart_id(request)
    )
    cart_item = CartItem.objects.get(cart=cart, product = product)
    if cart_item.quantity >1:
        cart_item.quantity -=1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')

def remove_cart_item(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_id = Cart.objects.get(
        cart_id = _cart_id(request)
    )
    
    try:
        cart_item = CartItem.objects.get(cart=cart_id, product=product)
        cart_item.delete()
    except CartItem.DoesNotExist:
        pass  
    return redirect('cart')

def cart(request):
    cart_id = Cart.objects.get(
        cart_id = _cart_id(request)
        )
    
    try:
        total = Decimal('0.00')
        cart_items = CartItem.objects.filter(cart = cart_id)
        for cart_item in cart_items:
            total += Decimal(cart_item.subtotal())
        tax = round(total * Decimal('0.10'), 2)
        total_with_tax = total+tax

    except CartItem.DoesNotExist:
        pass

    context ={
        'cart_items': cart_items,
        'cart_total_price': total,
        'tax': tax,
        'total_with_tax': total_with_tax,
    }

    return render(request, 'store/cart.html',context)


