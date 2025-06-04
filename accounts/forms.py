from django import forms
from . models import Accounts

class RegistrationFrom(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Enter Password'
        
    }))
    confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Confirm Password'
    }))
    class Meta:
        model=Accounts
        fields=['first_name','last_name','phone','email','password']
    
    def __init__(self,*args,**kwargs):
        super(RegistrationFrom,self).__init__(*args,**kwargs)
        self.fields['first_name'].widget.attrs['placeholder']='First Name'
        self.fields['last_name'].widget.attrs['placeholder']='Last Name'
        self.fields['phone'].widget.attrs['placeholder']='Phone Number'
        self.fields['email'].widget.attrs['placeholder']='Enter Email'
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'
            
    def clean(self):
        cleaned_data=super().clean()
        password= cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password != confirm_password:
            raise forms.ValidationError(
                "Password and Confirm Password does not exit"
            )


