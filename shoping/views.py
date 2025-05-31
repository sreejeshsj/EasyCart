from django.shortcuts import render
from store.models import Product
def Home(request):
    product=Product.objects.all().filter(is_available=True)
    context={
        'products':product
    }
    return render(request,'home.html',context)