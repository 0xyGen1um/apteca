from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404,redirect,render
from orders.models import Order
from .services import PaymentService

@login_required
def pay(request,order_id):
    order=get_object_or_404(Order,pk=order_id,user=request.user)
    if request.method=='POST':
        try:
            payment=PaymentService.pay(order,request.POST.get('outcome','success'),request.POST.get('transaction_id') or None,request.POST.get('last4',''),request.POST.get('card_brand',''))
            messages.success(request,f'Результат оплаты: {payment.get_status_display()}')
            return redirect('orders:detail',pk=order.pk)
        except ValueError as exc: messages.error(request,str(exc))
    return render(request,'payments/pay.html',{'order':order})
