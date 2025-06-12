from django.contrib import admin
from . models import Payment,OderProduct,Order
# Register your models here.
class OrderPorductInline(admin.TabularInline):
    model=OderProduct
    extra=0
class PaymentAdmin(admin.ModelAdmin):
    list_display=['user','payment_id','amount_paid','payment_method','status']
    
admin.site.register(Payment,PaymentAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display=['first_name','payment','status']
    inlines=[OrderPorductInline]
    
admin.site.register(Order,OrderAdmin)

class OrderPorductAdmin(admin.ModelAdmin):
    list_display=['product','payment','quantity','product_price']
    
admin.site.register(OderProduct,OrderPorductAdmin)