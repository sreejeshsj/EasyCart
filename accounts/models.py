from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
# Create your models here.
class MyAccountManager(BaseUserManager):
    def create_user(self,first_name,last_name,username,email,password=None):
        if not email:
            raise ValueError('User Modet have an Email')
        if not username:
            raise ValueError('User most have an Username')
        
        user=self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name
            
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
        
    def create_superuser(self,first_name,last_name,username,email,password=None):
        user=self.create_user(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password

        )
        
        user.is_admin=True
        user.is_staff=True
        user.is_active=True
        user.is_superadmin=True
        user.save(using=self._db)
        return user

class Accounts(AbstractBaseUser):
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    username=models.CharField(max_length=50)
    email=models.EmailField(max_length=100,unique=True)
    phone=models.CharField(max_length=10,unique=True)
    
    #required
    date_joined=models.DateTimeField(auto_now_add=True)
    last_login=models.DateTimeField(auto_now_add=True)
    
    is_admin=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    is_active=models.BooleanField(default=False)
    is_superadmin=models.BooleanField(default=False)
    
    USERNAME_FIELD='email'
    
    REQUIRED_FIELDS=['username','first_name','last_name']
    
    objects=MyAccountManager()
    
    def has_perm(self,perm,obj=None):
        return self.is_superadmin
    
    def has_module_perms(self,add_label):
        return self.is_superadmin
    
    class Meta:
        verbose_name='Accounts'
        verbose_name_plural='Accounts'
        
    def __str__(self):
        return self.email

        


