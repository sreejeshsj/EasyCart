from django.db import models
from store.models import Product

# Create your models here.
class Cart(models.Model):
    cart_id=models.CharField(max_length=250,blank=True)
    date_added=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='related_product')
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='related_cart')
    quantity=models.IntegerField()
    is_active=models.BooleanField(default=True)
    
    def sub_total(self):
        total=self.quantity*self.product.price
        return total
        
    def __str__(self):
        return self.product.product_name