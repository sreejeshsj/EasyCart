from django.shortcuts import render,redirect
from store.models import Product
from . models import Cart,CartItem
# Create your views here.
def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    
    return cart


def add_cart(request,product_id):
    product=Product.objects.get(id=product_id)
    try:
        
        cart=Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart=Cart.objects.create(
            cart_id=_cart_id(request)
        )
    cart.save()
    
    try:
        
        cart_item=CartItem.objects.get(product=product,cart=cart)
        cart_item.quantity +=1
    except CartItem.DoesNotExist:
        cart_item=CartItem.objects.create(
            product=product,
            cart=cart,
            quantity=1
        )
    cart_item.save()
    return redirect('cart')
def remove_cart(request,product_id):
    cart=Cart.objects.get(cart_id=_cart_id(request))
    product=Product.objects.get(id=product_id)
    cart_item=CartItem.objects.get(cart=cart,product=product)
    cart_item.delete()
    return redirect('cart')
def decrease(request,product_id):
    cart=Cart.objects.get(cart_id=_cart_id(request))
    product=Product.objects.get(id=product_id)
    cart_item=CartItem.objects.get(cart=cart,product=product)
    if cart_item.quantity >1 :
        cart_item.quantity-=1
    cart_item.save()
    return redirect('cart')
        
def cart(request):
    total=0
    
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_items=CartItem.objects.filter(cart=cart,is_active=True)
        
        for cart_item in cart_items:
           
            total+=cart_item.product.price * cart_item.quantity
        tax=(2*total)/100
        grand_total=tax+total
        
    except Cart.DoesNotExist:
        raise ValueError('Not')
    context={
        'cart_items':cart_items,
        'total':total,
        'grand_total':grand_total,
        'tax':tax,
        
        
    }
    return render(request,'store/cart.html',context)
    