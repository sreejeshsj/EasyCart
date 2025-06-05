from django.urls import path
from . import views

urlpatterns=[
    path('register/',views.register,name="register"),
    path('login/',views.login_view,name="login"),
    path('logout/',views.logout_view,name="logout"),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('',views.dashboard,name='dashboard'),
    path('forgotpassword/',views.forgot_password,name='forgotpassword'),
    path('activate/<uidb64>/<token>/',views.activate,name='activate'),
    path('resetpassword_validate/<uidb64>/<token>/',views.reset,name='resetpassword_validate'),
    path('resetpassword/',views.reset_password,name='resetpassword'),
]