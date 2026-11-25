from django.db import models
from django.db.models import Q
from enums import PaymentMethodType,PaymentStatus

class Payment(models.Model):
    order=models.ForeignKey('orders.Order',on_delete=models.CASCADE,related_name='payments')
    amount=models.DecimalField(max_digits=10,decimal_places=2)
    method=models.CharField(max_length=10,choices=PaymentMethodType.choices)
    status=models.CharField(max_length=10,choices=PaymentStatus.choices,default=PaymentStatus.PENDING)
    created_at=models.DateTimeField(auto_now_add=True)
    completed_at=models.DateTimeField(null=True,blank=True)
    transaction_id=models.CharField(max_length=100,unique=True)
    last4=models.CharField(max_length=4,blank=True)
    card_brand=models.CharField(max_length=30,blank=True)
    class Meta:
        constraints=[models.CheckConstraint(condition=Q(amount__gte=0),name='payment_amount_nonnegative')]
