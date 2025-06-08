from django.urls import path
from . import views
urlpatterns=[
    path('',views.cart,name='cart'),
    path('add_cart/<int:product_id>/',views.add_cart,name='add_cart'),
    path('remove_cart/<int:cart_item_id>/',views.remove_cart,name='remove_cart'),
    path('decrease/<int:cart_item_id>/',views.decrease,name='decrease'),
    path('increase/<int:cart_item_id>/',views.increase,name='increase'),
    path('checkout/',views.checkout,name='checkout')
    
]