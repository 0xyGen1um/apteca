from django.db import transaction
from django.utils import timezone
from enums import PrescriptionStatus,UserRole,OrderStatus
from .models import Prescription

class PrescriptionService:
    @staticmethod
    def submit(order,product,image):
        if not image: raise ValueError('Загрузите рецепт')
        return Prescription.objects.create(order=order,product=product,image=image)
    @staticmethod
    @transaction.atomic
    def approve(prescription,reviewer):
        if reviewer.role not in (UserRole.PHARMACIST,UserRole.ADMIN): raise PermissionError('Недостаточно прав')
        p=Prescription.objects.select_for_update().get(pk=prescription.pk)
        if p.status!=PrescriptionStatus.PENDING: raise ValueError('Рецепт уже проверен')
        p.status=PrescriptionStatus.APPROVED;p.reviewed_by=reviewer;p.reviewed_at=timezone.now();p.save()
        if not p.order.prescriptions.exclude(status=PrescriptionStatus.APPROVED).exists():
            p.order.status=OrderStatus.NEW;p.order.save(update_fields=['status'])
            from enums import PaymentMethodType
            if p.order.payment_method==PaymentMethodType.CASH:
                from payments.services import PaymentService
                PaymentService.pay(p.order)
        return p
    @staticmethod
    @transaction.atomic
    def reject(prescription,reviewer,reason):
        if reviewer.role not in (UserRole.PHARMACIST,UserRole.ADMIN): raise PermissionError('Недостаточно прав')
        if not reason or not reason.strip(): raise ValueError('Укажите причину отказа')
        p=Prescription.objects.select_for_update().get(pk=prescription.pk)
        if p.status!=PrescriptionStatus.PENDING: raise ValueError('Рецепт уже проверен')
        p.status=PrescriptionStatus.REJECTED;p.rejection_reason=reason.strip();p.reviewed_by=reviewer;p.reviewed_at=timezone.now();p.save()
        from orders.services import OrderService
        OrderService.cancel(p.order)
        return p
