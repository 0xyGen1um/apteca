from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect,render
from .services import CartService

@login_required
def detail(request):
    cart=CartService.get_cart(request.user)
    return render(request,'cart/detail.html',{'cart':cart,'total':CartService.calculate_total(cart)})

@login_required
def change(request,product_id):
    if request.method=='POST':
        try:
            action=request.POST.get('action')
            if action=='remove': CartService.remove_item(request.user,product_id)
            elif action=='update': CartService.update_quantity(request.user,product_id,int(request.POST.get('quantity',1)))
            else: CartService.add_item(request.user,product_id,int(request.POST.get('quantity',1)))
        except (ValueError,TypeError,Exception) as exc: messages.error(request,str(exc))
    return redirect(request.POST.get('next') or 'cart:detail')
