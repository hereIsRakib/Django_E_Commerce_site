from .models import Cart, CartItem
from .views import _cart_id


def cart_item_total(request):
    quantity = 0
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.all().filter(user = request.user)

        else:
        
            cart = Cart.objects.get(
                cart_id = _cart_id(request)
            )
                
            cart_items = CartItem.objects.filter(cart = cart)

        for cart_item in cart_items:
            quantity+=cart_item.quantity

    except Cart.DoesNotExist:
        quantity = 0
    return dict(cart_item_total= quantity)