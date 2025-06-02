from . models import Cart,CartItem
from store.models import Product
from . views import _cart_id
def count_item(request):
    cart=Cart.objects.filter(cart_id=_cart_id(request)).first()
    cart_items=CartItem.objects.filter(cart=cart,is_active=True)
    count_cart=cart_items.count()
    
    return dict(count_cart=count_cart)
        