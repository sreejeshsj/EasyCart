from django.contrib import admin
from . models import Product,Variations
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields={  'slug':('product_name',) }
    list_display=('product_name','price','stock','category','modified_date','is_available',)
admin.site.register(Product,ProductAdmin)

class VariationAdmin(admin.ModelAdmin):
    list_display=('product','variation_category','variation_value','created_date','is_active')
    list_filter=('product','variation_category','variation_value','created_date','is_active')
    list_editable=('is_active',)
admin.site.register(Variations,VariationAdmin)
    
