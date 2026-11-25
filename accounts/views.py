from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView,LogoutView
from django.shortcuts import render,redirect
from .forms import RegisterForm,ProfileForm

def register(request):
    form=RegisterForm(request.POST or None)
    if request.method=='POST' and form.is_valid():
        user=form.save();login(request,user);return redirect('catalog:home')
    return render(request,'accounts/form.html',{'form':form,'title':'Регистрация'})

class SignInView(LoginView):
    template_name='accounts/form.html'
    extra_context={'title':'Вход'}

class SignOutView(LogoutView): pass

@login_required
def profile(request):
    form=ProfileForm(request.POST or None,instance=request.user)
    if request.method=='POST' and form.is_valid(): form.save();messages.success(request,'Профиль сохранён');return redirect('accounts:profile')
    return render(request,'accounts/profile.html',{'form':form,'orders':request.user.orders.order_by('-created_at').prefetch_related('items')})
