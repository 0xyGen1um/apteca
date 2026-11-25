from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404,redirect,render
from django.http import HttpResponseForbidden
from enums import UserRole,PrescriptionStatus
from .models import Prescription
from .services import PrescriptionService

@login_required
def queue(request):
    if request.user.role not in (UserRole.PHARMACIST,UserRole.ADMIN): return HttpResponseForbidden('Нет доступа')
    if request.method=='POST':
        item=get_object_or_404(Prescription,pk=request.POST.get('id'))
        try:
            if request.POST.get('action')=='approve': PrescriptionService.approve(item,request.user)
            else: PrescriptionService.reject(item,request.user,request.POST.get('reason',''))
            messages.success(request,'Рецепт проверен')
        except (ValueError,PermissionError) as exc: messages.error(request,str(exc))
    return render(request,'prescriptions/queue.html',{'items':Prescription.objects.filter(status=PrescriptionStatus.PENDING).select_related('order','product')})
