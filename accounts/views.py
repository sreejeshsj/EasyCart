from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from . forms import RegistrationFrom
from . models import Accounts
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
import requests
#verifiction
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail,EmailMessage
from carts.models import Cart,CartItem
from carts.views import _cart_id
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
            #USER ACTIVATION
            current_site = get_current_site(request)
            mail_subject='Please activate your account'
            message=render_to_string('accounts/account_verification_email.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email=email
            send_email=EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            #messages.success(request,'Thank you for Registring with us, we have sent an verifiaction email to your email please verify to activate your account!')
            return redirect('/accounts/login/?command=verification&email='+email)
    else:
            
            
            form = RegistrationFrom()
    
    
    context={
        'form':form
    }
    return render(request,'accounts/register.html',context)

def login_view(request):
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']
        user=authenticate(request, username=email, password=password)
        if user is not None:
            try:
                guest_cart=Cart.objects.get(cart_id=_cart_id(request))
                guest_cart_items=CartItem.objects.filter(cart=guest_cart)
                print("this is guest cart:",guest_cart)
                user_cart,_=Cart.objects.get_or_create(user=user)
                print("this is user :",user_cart)
                for guest_item in guest_cart_items:
                    existing_items=CartItem.objects.filter(
                        user=user,
                        cart=user_cart,
                        product=guest_item.product,
                    )
                    merged=False
                    for existing_item in existing_items:
                        if set(existing_item.variations.all()) == set(guest_item.variations.all()):
                            existing_item.quantity+=guest_item.quantity
                            
                            existing_item.save()
                            merged=True
                            break
                    if not merged:
                        guest_item.user=user
                        guest_item.cart=user_cart
                        
                        guest_item.save()
               
                guest_cart.delete()
                
                
                
                    
            except Cart.DoesNotExist:
                pass
                
            login(request,user)
            messages.success(request,'You are now logged in')
            url=request.META.get('HTTP_REFERER')
            try:
                query=requests.utils.urlparse(url).query
                print(query)
                params = dict(x.split('=') for x in query.split('&'))
                print(params)
                if 'next' in params:
                    nextPage=params['next']
                    return redirect(nextPage)
                
            except:
                return redirect('dashboard')
            
        else:
            messages.error(request,'Invalid login Credintials')
            return redirect('login')
        
            
        
    return render(request,'accounts/login.html')
@login_required(login_url='login')
def logout_view(request):
    logout(request)
    messages.success(request,'success')
    return redirect('login')

def activate(request,uidb64,token):
    try:
       uid=urlsafe_base64_decode(uidb64).decode()
       user=Accounts.objects.get(id=uid)
    except(TypeError,ValueError,OverflowError,Accounts.DoesNotExist):
        user=None
        pass
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        messages.success(request,'Congrates you account is activated')
        return redirect('login')
    else:
        messages.error(request,'Invalid Activation Link')
        return redirect('register')
        
    return HttpResponse('ok')

@login_required(login_url='login')
def dashboard(request):
    return render(request,'accounts/dashboard.html')


def forgot_password(request):
    if request.method=='POST':
        email=request.POST['email']
        if Accounts.objects.filter(email=email).exists():
            user=Accounts.objects.get(email__exact=email)
            #Reset password functionality
            current_site=get_current_site(request)
            mail_subject='Reset Password Link'
            message=render_to_string('accounts/password_reset.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email=email
            send_mail=EmailMessage(mail_subject,message,to=[to_email])
            send_mail.send()
            messages.success(request,'Password reset email has been sent to your email address')
            return redirect('login')
            
        else:
            messages.error(request,'Account Does not Exist')
            return redirect('register')
    return render(request,'accounts/forgotPassword.html')

def reset(request,uidb64,token):
    try:
       uid=urlsafe_base64_decode(uidb64).decode()
       user=Accounts.objects.get(id=uid)
    except(TypeError,ValueError,OverflowError,Accounts.DoesNotExist):
        user=None
        pass
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid']=uid
        messages.success(request,'Please reset your password')
        return redirect('resetpassword')
    else:
        messages.error(request,'Link is expired')
        return redirect('login')
    
    return HttpResponse('ok')

def reset_password(request):
    if request.method=='POST':
        password=request.POST['password']
        confirm_password=request.POST['confirmpassword']
        if password==confirm_password:
            uid=request.session.get('uid')
            user=Accounts.objects.get(id=uid)
            user.set_password(password)
            user.save()
            messages.success(request,'password reset successfully')
            return redirect('login')
        else:
            messages.error(request,'password do not match ')
            return redirect('resetpassword')
    else:
        
        return render(request,'accounts/resetPassword.html')