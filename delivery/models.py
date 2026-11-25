from django.conf import settings
from django.db import models

class PickupPoint(models.Model):
    name=models.CharField(max_length=150)
    address=models.TextField()
    is_active=models.BooleanField(default=True)
    def __str__(self): return self.name

class DeliveryAddress(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    address=models.TextField()

class Delivery(models.Model):
    class Method(models.TextChoices):
        PICKUP='PICKUP','Самовывоз'; COURIER='COURIER','Курьер'
    class Status(models.TextChoices):
        NEW='NEW','Новая'; READY='READY','Готово'; OUT='OUT','В пути'; DELIVERED='DELIVERED','Доставлено'
    order=models.OneToOneField('orders.Order',on_delete=models.CASCADE,related_name='delivery')
    method=models.CharField(max_length=10,choices=Method.choices)
    status=models.CharField(max_length=12,choices=Status.choices,default=Status.NEW)
    pickup_point=models.ForeignKey(PickupPoint,on_delete=models.PROTECT,null=True,blank=True)
    delivery_address=models.ForeignKey(DeliveryAddress,on_delete=models.PROTECT,null=True,blank=True)
