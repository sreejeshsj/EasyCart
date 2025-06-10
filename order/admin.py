from django.contrib import admin
from . models import Payment,OderProduct,Order
# Register your models here.

class PaymentAdmin(admin.ModelAdmin):
    list_display=['user','payment_id','amount_paid','payment_method','status']
    
admin.site.register(Payment,PaymentAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display=['first_name','payment','status']
    
admin.site.register(Order,OrderAdmin)

class OrderPorductAdmin(admin.ModelAdmin):
    list_display=['user','payment','quantity']
    
admin.site.register(OderProduct,OrderPorductAdmin)