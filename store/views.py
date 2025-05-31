from django.shortcuts import render,get_object_or_404
from . models import Product
from category.models import Category
# Create your views here.

def store(request,category_slug=None):
    categories=None
    product=None

    if category_slug:
        categories=get_object_or_404(Category,slug=category_slug.lower())
        product=Product.objects.filter(category=categories,is_available=True)
        count=product.count()
    else:
        product = Product.objects.all().filter(is_available=True)
        count=product.count()
        print(count)
    context={
        'products':product,
        'count':count
    }
    return render(request,'store/store.html',context)

def product_details(request,category_slug,product_slug):
    try:
        single_product=Product.objects.get(category__slug=category_slug,slug=product_slug)
        context={
            'single_product':single_product
        }
        
    except Product.DoesNotExist:
        raise ValueError("Not exists")
    return render(request,'store/product_details.html',context)
