from django.shortcuts import render,redirect
from store.models import Product,Variations
from . models import Cart,CartItem
from django.shortcuts import HttpResponse

# Create your views here.
def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    
    return cart


def add_cart(request,product_id):
    product_variations=[]
    product=Product.objects.get(id=product_id)
    if request.method=='POST':
        for item in request.POST:
            key=item
            value=request.POST[key]
            try:
                variation=Variations.objects.get(product=product,variation_category__iexact=key,variation_value__iexact=value)
                product_variations.append(variation)
            except:
                pass
   
    
    
    try:
        
        cart=Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart=Cart.objects.create(
            cart_id=_cart_id(request)
        )
    cart.save()
    
    
        
    cart_item=CartItem.objects.filter(product=product,cart=cart)
    item_found=False
    for item in cart_item:
        existing_variation=list(item.variations.all())
        print(existing_variation)
        if set(existing_variation)==set(product_variations):
            item.quantity+=1
            item.save()
            item_found=True
            break
    if not item_found:
        cart_item=CartItem.objects.create(
            product=product,
            cart=cart,
            quantity=1,
            )
        if product_variations:
            cart_item.variations.set(product_variations)
        cart_item.save()
    return redirect('cart')
def remove_cart(request,cart_item_id):
    cart=Cart.objects.get(cart_id=_cart_id(request))
    cart_item=CartItem.objects.get(id=cart_item_id,cart=cart)
    cart_item.delete()
    return redirect('cart')
def decrease(request,cart_item_id):
    cart=Cart.objects.get(cart_id=_cart_id(request))
    cart_item=CartItem.objects.get(cart=cart,id=cart_item_id)
    if cart_item.quantity >1 :
        cart_item.quantity-=1
    cart_item.save()
    return redirect('cart')

def increase(request,cart_item_id):
    cart=Cart.objects.get(cart_id=_cart_id(request))
    cart_item=CartItem.objects.get(cart=cart,id=cart_item_id)
    cart_item.quantity+=1
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
    