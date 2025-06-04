from django.shortcuts import render,redirect
from . forms import RegistrationFrom
from . models import Accounts
from django.contrib import messages
# Create your views here.

def register(request):
    if request.method=='POST':
        form=RegistrationFrom(request.POST)
        
        if form.is_valid():
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            phone=form.cleaned_data['phone']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            username=email.split('@')[0]
            user=Accounts.objects.create_user(first_name=first_name,last_name=last_name,email=email,password=password,username=username)
            user.phone=phone
            user.save()
            messages.success(request,'Registration Successfull')
            return redirect('register')
    else:
            
            
            form = RegistrationFrom()
    
    
    context={
        'form':form
    }
    return render(request,'accounts/register.html',context)

def login(request):
    return render(request,'accounts/login.html')

def logout(request):
    return 