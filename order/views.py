from django.shortcuts import render,redirect
from carts.models import Cart,CartItem
from . forms import OrderForm
from . models import Order,Payment,OderProduct
from datetime import datetime,date
import json
# Create your views here.

def payment(request):
    body=json.loads(request.body)
    order=Order.objects.get(user=request.user,is_ordered=False,order_number=body['orderId'])
    payment=Payment(
         user=request.user,
         payment_id=body['transationId'],
         payment_method=body['payment_method'],
         status=body['status'],
         amount_paid=body['amount']
        
    )
    payment.save()
    order.payment=payment
    order.is_ordered=True
    order.save()
    cart_items=CartItem.objects.filter(user=request.user)
    print(cart_items)
    for cart_item in cart_items:
        order_product=OderProduct()
        order_product.order_id=order.id
        order_product.user_id=request.user.id
        order_product.payment=payment
        order_product.product_id=cart_item.product_id
        order_product.quantity=cart_item.quantity
        order_product.product_price=cart_item.product.price
        order_product.ordered=True
        order_product.save()
        item=CartItem.objects.get(id=cart_item.id)
        order_product.variations.set(item.variations.all())
        order_product.save()
    return render(request,'orders/payment.html')

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
           
            
            order=Order.objects.get(user=current_user,is_ordered=False,order_number=order_number)
            
            context={
                'order':order,
                'cart_items':cart_items,
                'tottal':total,
                'tax':tax,
                'grand_total':grand_total
            }
            return render(request,'orders/payment.html',context)
        
        else:
            print('not valid')
            return redirect('checkout')
            
            
            
        
        
