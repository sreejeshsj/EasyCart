from django.shortcuts import render,redirect
from carts.models import Cart,CartItem
from . forms import OrderForm
from . models import Order
from datetime import datetime,date
# Create your views here.

def place_order(request):
    current_user=request.user
    cart_items=CartItem.objects.filter(user=current_user)
    if cart_items.count() <=0:
        return redirect('store') 
    total=0
    for i in cart_items:
        total+=i.product.price
    tax=(2*total)/100
    grand_total=total+tax
    if request.method=='POST':
        print("times")
        form = OrderForm(request.POST)
        if form.is_valid():
            
            data = Order()
            data.user=current_user
            data.first_name=form.cleaned_data['first_name']
            data.last_name=form.cleaned_data['last_name']
            data.phone=form.cleaned_data['phone']
            data.email=form.cleaned_data['email']
            data.address_line_1=form.cleaned_data['address_line_1']
            data.address_line_2=form.cleaned_data['address_line_2']
            data.country=form.cleaned_data['country']
            data.state=form.cleaned_data['state']
            data.city=form.cleaned_data['city']
            data.order_note=form.cleaned_data['order_note']
            data.order_total=grand_total
            data.tax=tax
            data.ip=request.META.get('REMOTE_ADDR')
            data.save()
            
            #ordernumber generation
            
            year=int(datetime.today().strftime('%Y'))
            day=int(datetime.today().strftime('%d'))
            month=int(datetime.today().strftime('%m'))
            d=date(year,month,day)
            current_date=d.strftime("%Y%m%d")
            order_number=current_date + str(data.id)
            data.order_number=order_number
            data.save()
            print(data)
            return redirect('checkout')
        
        else:
            print('not valid')
            return redirect('checkout')
            
            
            
        
        
