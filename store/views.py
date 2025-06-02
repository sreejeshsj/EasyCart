from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from . models import Product
from category.models import Category
from carts.models import CartItem
from carts.views import _cart_id
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
# Create your views here.


def store(request,category_slug=None):
    categories=None
    product=None

    if category_slug:
        categories=get_object_or_404(Category,slug=category_slug.lower())
        product=Product.objects.filter(category=categories ,is_available=True).order_by('id')
        count=product.count()
        paginator=Paginator(product,2)
        page=request.GET.get('page')
        paged_product=paginator.get_page(page)
    else:
        product = Product.objects.all().filter( is_available=True,).order_by('id')
        paginator=Paginator(product,2)
        page=request.GET.get('page')
        paged_product=paginator.get_page(page)
        count=product.count()
        
    context={
        'products':paged_product,
        'count':count
    }
    return render(request,'store/store.html',context)

def product_details(request,category_slug,product_slug):
    try:
        single_product=Product.objects.get(category__slug=category_slug,slug=product_slug)
        in_cart=CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists() 
        context={
            'single_product':single_product,
            'in_cart':in_cart
        }
    
    
    except Product.DoesNotExist:
        raise ValueError("Not exists")
    
    
    return render(request,'store/product_details.html',context)

def search(request):
    keyword=request.GET.get('keyword','').strip()
    product = Product.objects.none() 
    if keyword:
        product=Product.objects.filter(slug__icontains=keyword,is_available=True).order_by('id')    
    paginator=Paginator(product,2)
    page=request.GET.get('page')
    paged_product=paginator.get_page(page)
    count=product.count()
    
    context={
        'products':paged_product,
        'count':count,
        'keyword':keyword,
    }
    return render(request,'store/store.html',context)

