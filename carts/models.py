from django.db import models
from store.models import Product,Variations
from accounts.models import Accounts
# Create your models here.
class Cart(models.Model):
    cart_id=models.CharField(max_length=250,blank=True)
    user=models.ForeignKey(Accounts,on_delete=models.CASCADE,null=True)
    date_added=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
       if self.user is not None:
            return self.user.first_name
       else:
           return self.cart_id
        

class CartItem(models.Model):
    user = models.ForeignKey(Accounts,on_delete=models.CASCADE,null=True)
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='related_product')
    variations=models.ManyToManyField(Variations,blank=True)
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='related_cart')
    quantity=models.IntegerField()
    is_active=models.BooleanField(default=True)
    
    def sub_total(self):
        total=self.quantity*self.product.price
        return total
        
    def __str__(self):
        return self.product.product_name

