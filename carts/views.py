from django.shortcuts import render,redirect
from store.models import Product,Variations
from . models import Cart,CartItem
from django.shortcuts import HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.
def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    
    return cart


def add_cart(request,product_id):
    current_user=request.user
    
    product=Product.objects.get(id=product_id)
    #if user is authenticated
   
    if current_user.is_authenticated:
            
            cart,created=Cart.objects.get_or_create(user=current_user)
    else:
            cart,created=Cart.objects.get_or_create(cart_id=_cart_id(request))
   
    if current_user.is_authenticated:
        product_variations=[]
        if request.method=='POST':
            for item in request.POST:
                key=item
                value=request.POST[key]
                try:
                    variation=Variations.objects.get(product=product,variation_category__iexact=key,variation_value__iexact=value)
                    product_variations.append(variation)
                except:
                    pass
        
        cart_item=CartItem.objects.filter(product=product,user=current_user,cart=cart)
        item_found=False
        for item in cart_item:
            existing_variation=list(item.variations.all())
           
            if set(existing_variation)==set(product_variations):
                item.quantity+=1
                item.save()
                item_found=True
                break
        if not item_found:
            cart_item=CartItem.objects.create(
                product=product,
                quantity=1,
                cart=cart,
                user=current_user,
                )
            if product_variations:
                cart_item.variations.set(product_variations)
            cart_item.save()
        return redirect('cart')
    else:
        
        product_variations=[]
        if request.method=='POST':
            for item in request.POST:
                key=item
                value=request.POST[key]
                try:
                    variation=Variations.objects.get(product=product,variation_category__iexact=key,variation_value__iexact=value)
                    product_variations.append(variation)
                except:
                    pass   
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
    print(cart_item_id)
    
    cart_item=CartItem.objects.get(id=cart_item_id)
    if request.user.is_authenticated:
        if cart_item.user==request.user:
            cart_item.delete()
    else:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        if cart_item.cart==cart:
            cart_item.delete()
    print(cart_item)
    
    return redirect('cart')
def decrease(request,cart_item_id):
    
    cart_item=CartItem.objects.get(id=cart_item_id)
    if cart_item.quantity >1 :
        cart_item.quantity-=1
    cart_item.save()
    return redirect('cart')

def increase(request,cart_item_id):
    
    cart_item=CartItem.objects.get(id=cart_item_id)
    cart_item.quantity+=1
    cart_item.save()
    return redirect('cart')
        
def cart(request):
    total=0
    
    try:
        if request.user.is_authenticated:
            cart_items=CartItem.objects.filter(user=request.user,is_active=True)
        
        else:
            cart=Cart.objects.get(cart_id=_cart_id(request))
            cart_items=CartItem.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items:
           
            total+=cart_item.product.price * cart_item.quantity
        tax=(2*total)/100
        grand_total=tax+total
        
    except Cart.DoesNotExist:
        return render(request,'store/cart.html')
    context={
        'cart_items':cart_items,
        'total':total,
        'grand_total':grand_total,
        'tax':tax,
        
        
    }
    return render(request,'store/cart.html',context)


@login_required(login_url='login')
def checkout(request):
    total=0
    try:
        cart=Cart.objects.get(user=request.user)
        cart_items=CartItem.objects.filter(cart=cart,user=request.user,is_active=True)
        
        for cart_item in cart_items:
           
            total+=cart_item.product.price * cart_item.quantity
        tax=(2*total)/100
        grand_total=tax+total
        
    except Cart.DoesNotExist:
        return render(request,'store/cart.html')
    context={
        'cart_items':cart_items,
        'total':total,
        'grand_total':grand_total,
        'tax':tax,
        
        
    }
    return render(request,'store/checkout.html',context)
    