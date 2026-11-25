from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseForbidden
from enums import UserRole
from .models import Delivery

@login_required
def dashboard(request):
    if request.user.role not in (UserRole.COURIER,UserRole.ADMIN): return HttpResponseForbidden('Нет доступа')
    return render(request,'delivery/dashboard.html',{'deliveries':Delivery.objects.filter(method=Delivery.Method.COURIER).select_related('order','delivery_address')})
