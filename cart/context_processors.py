from .models import Cart, CartItem
from .views import _cart_id


def cart_item_total(request):
    quantity = 0
    try:
        cart_id = Cart.objects.get(
            cart_id = _cart_id(request)
        )
        cart_items = CartItem.objects.filter(cart_id = cart_id)

        for cart_item in cart_items:
            quantity+=cart_item.quantity

    except Cart.DoesNotExist:
        quantity = 0
    return dict(cart_item_total= quantity)