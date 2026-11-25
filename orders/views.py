from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseForbidden
from enums import OrderStatus,UserRole
from cart.services import CartService
from .forms import CheckoutForm
from .models import Order
from .services import OrderService

@login_required
def checkout(request):
    form=CheckoutForm(request.POST or None,request.FILES or None)
    cart=CartService.get_cart(request.user)
    if request.method=='POST' and form.is_valid():
        d=form.cleaned_data
        try:
            order=OrderService.create_from_cart(request.user,d['payment_method'],d['delivery_method'],d['address'],d['pickup_point'].pk if d['pickup_point'] else None,d['prescription_image'],d['comment'])
            messages.success(request,'Заказ оформлен')
            return redirect('orders:detail',pk=order.pk)
        except (ValueError,Exception) as exc: messages.error(request,str(exc))
    return render(request,'orders/checkout.html',{'form':form,'total':CartService.calculate_total(cart),'items':cart.items.select_related('product')})

@login_required
def detail(request,pk):
    order=get_object_or_404(Order.objects.prefetch_related('items__product','prescriptions','payments'),pk=pk)
    if order.user_id!=request.user.pk and request.user.role not in (UserRole.ADMIN,UserRole.PHARMACIST,UserRole.COURIER): return HttpResponseForbidden('Нет доступа')
    return render(request,'orders/detail.html',{'order':order})

@login_required
def cancel(request,pk):
    if request.method=='POST':
        order=get_object_or_404(Order,pk=pk,user=request.user)
        try: OrderService.cancel(order);messages.success(request,'Заказ отменён')
        except ValueError as exc: messages.error(request,str(exc))
    return redirect('orders:detail',pk=pk)

@login_required
def manage(request):
    if request.user.role not in (UserRole.ADMIN,UserRole.PHARMACIST,UserRole.COURIER): return HttpResponseForbidden('Нет доступа')
    if request.method=='POST':
        order=get_object_or_404(Order,pk=request.POST.get('order_id'))
        try: OrderService.change_status(order,request.POST.get('status'));messages.success(request,'Статус изменён')
        except ValueError as exc: messages.error(request,str(exc))
    return render(request,'orders/manage.html',{'orders':Order.objects.exclude(status__in=[OrderStatus.CANCELLED,OrderStatus.COMPLETED]).order_by('-created_at'),'statuses':OrderStatus.choices})
