from django.db import models
from accounts.models import Accounts
from store.models import Product,Variations
# Create your models here.

class Payment(models.Model):
    user=models.ForeignKey(Accounts,on_delete=models.CASCADE)
    payment_id=models.CharField(max_length=100)
    payment_method=models.CharField(max_length=100)
    amount_paid=models.CharField(max_length=100)
    status=models.CharField(max_length=100)
    ceated_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.payment_id


class Order(models.Model):
    STATUS=(
        ('New','New'),
        ('Accepted','Accepted'),
        ('Completed','Completed'),
        ('Cancelled','Cancelled')
    )
    user = models.ForeignKey(Accounts,on_delete=models.SET_NULL,null=True)
    payment= models.ForeignKey(Payment,on_delete=models.SET_NULL,blank=True,null=True)
    order_number=models.CharField(max_length=20)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    email=models.EmailField(max_length=100)
    phone=models.CharField(max_length=10)
    address_line_1=models.CharField(max_length=50)
    address_line_2=models.CharField(max_length=50,blank=True)
    country = models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    city=models.CharField(max_length=50)
    order_note=models.CharField(max_length=100,blank=True)
    order_total=models.FloatField()
    tax=models.FloatField()
    status=models.CharField(max_length=10,choices=STATUS,default='New')
    ip=models.CharField(blank=True,max_length=20)
    is_ordered=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    
    
    def full_name(self):
        return self.first_name +" "+ self.last_name
    
    def __str__(self):
        return self.order_number
    
class OderProduct(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(Accounts,on_delete=models.CASCADE,null=True)
    payment= models.ForeignKey(Payment,on_delete=models.SET_NULL,blank=True,null=True)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    variations=models.ManyToManyField(Variations,blank=True)
    quantity= models.IntegerField()
    product_price=models.FloatField()
    ordered=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.product.product_name