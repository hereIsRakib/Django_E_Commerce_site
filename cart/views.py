from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from store.models import Product
from .models import Cart, CartItem
from decimal import Decimal
from django.core.exceptions import ObjectDoesNotExist
from store.models import Variation

def _cart_id(request):
    
    cart_id = request.session.session_key
    
    if not cart_id:
        cart_id = request.session.create()
    return cart_id

def add_cart(request,product_id):
    product = Product.objects.get(id = product_id)
    product_variation = []
    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]

            try:
                variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact = value)
                product_variation.append(variation)

            except:
                pass


    try:
        cart = Cart.objects.get(
            cart_id = _cart_id(request)
            )
        
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )

    is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
    if is_cart_item_exists:
        cart_item= CartItem.objects.filter(product=product, cart = cart)

        ex_var_list= []
        id=[]
        for item in cart_item:
            existing_variation = list(item.variations.all().order_by('id'))
            ex_var_list.append(list(existing_variation))
            id.append(item.id)
        product_variation = sorted(product_variation, key=lambda v: v.id)
        if product_variation in ex_var_list:
            index = ex_var_list.index(product_variation)
            item_id=id[index]
            item =CartItem.objects.get(product= product, id=item_id)
            item.quantity+=1
            item.save()
        else:
            item= CartItem.objects.create(
                product=product,
                quantity = 1,
                cart=cart
            )
            if len(product_variation)>0:
                item.variations.clear()
                item.variations.add(*product_variation) 
            item.save()
            

            

    else:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart
        )
        if len(product_variation)>0:
            cart_item.variations.clear()
            cart_item.variations.add(*product_variation)
        cart_item.save()

    return redirect("cart")

def minus_cart_item(request,product_id, cart_item_id):
    product = get_object_or_404(Product, id= product_id)
    cart = Cart.objects.get(
        cart_id = _cart_id(request)
    )
    try:
        cart_item = CartItem.objects.get(cart=cart, product = product, id=cart_item_id)
        if cart_item.quantity >1:
            cart_item.quantity -=1
            cart_item.save()
        else:
            cart_item.delete()

    except:
        pass

    return redirect('cart')

def remove_cart_item(request, product_id,cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    cart_id = Cart.objects.get(
        cart_id = _cart_id(request)
    )
    
    try:
        cart_item = CartItem.objects.get(cart=cart_id, product=product, id= cart_item_id)
        cart_item.delete()
    except CartItem.DoesNotExist:
        pass  
    return redirect('cart')

def cart(request):
    total = Decimal('0.00')
    tax = Decimal('0.00')
    total_with_tax = Decimal('0.00')
    cart_items=[]
    
    try:
        cart_id = Cart.objects.get(
            cart_id = _cart_id(request)
            )
        total = Decimal('0.00')
        cart_items = CartItem.objects.filter(cart = cart_id, is_active = True)
        for cart_item in cart_items:
            total += Decimal(cart_item.subtotal())
        tax = round(total * Decimal('0.10'), 2)
        total_with_tax = total+tax

    except ObjectDoesNotExist:
        pass

    context ={
        'cart_items': cart_items,
        'cart_total_price': total,
        'tax': tax,
        'total_with_tax': total_with_tax,
    }

    return render(request, 'store/cart.html',context)


