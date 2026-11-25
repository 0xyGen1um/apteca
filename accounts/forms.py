from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class RegisterForm(UserCreationForm):
    class Meta:
        model=User;fields=['email','user_name','birth_date','phone','password1','password2']
        widgets={'birth_date':forms.DateInput(attrs={'type':'date'})}

class ProfileForm(forms.ModelForm):
    class Meta:
        model=User;fields=['user_name','birth_date','phone']
        widgets={'birth_date':forms.DateInput(attrs={'type':'date'})}
