from . models import Cart,CartItem
from store.models import Product
from . views import _cart_id
def count_item(request):
    
    try:
        cart= Cart.objects.filter(cart_id=_cart_id(request)).first()
        if request.user.is_authenticated:
            cart_items=CartItem.objects.filter(user=request.user)
        else:
            cart_items=CartItem.objects.filter(cart=cart,is_active=True)
    except Cart.DoesNotExist:
        count_cart=0
    
    
    count_cart=cart_items.count()
    
    return dict(count_cart=count_cart)
        