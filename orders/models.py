from django.conf import settings
from django.db import models
from django.db.models import Q
from enums import OrderStatus,PaymentMethodType

class Order(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name='orders')
    created_at=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=30,choices=OrderStatus.choices,default=OrderStatus.NEW)
    total_amount=models.DecimalField(max_digits=10,decimal_places=2)
    address=models.TextField(blank=True)
    comment=models.TextField(blank=True)
    payment_method=models.CharField(max_length=10,choices=PaymentMethodType.choices)
    stock_written_off=models.BooleanField(default=False)
    class Meta:
        constraints=[models.CheckConstraint(condition=Q(total_amount__gte=0),name='order_amount_nonnegative')]

class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items')
    product=models.ForeignKey('catalog.Product',on_delete=models.PROTECT)
    quantity=models.PositiveIntegerField()
    unit_price=models.DecimalField(max_digits=10,decimal_places=2)
    class Meta:
        constraints=[models.CheckConstraint(condition=Q(quantity__gt=0),name='order_quantity_positive'),models.CheckConstraint(condition=Q(unit_price__gte=0),name='unit_price_nonnegative')]
