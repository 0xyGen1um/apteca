from django.db import transaction
from .models import Delivery,DeliveryAddress,PickupPoint

class DeliveryService:
    @staticmethod
    def create(order,method,address='',pickup_point_id=None):
        if method==Delivery.Method.PICKUP:
            point=PickupPoint.objects.get(pk=pickup_point_id,is_active=True)
            return Delivery.objects.create(order=order,method=method,pickup_point=point)
        if method==Delivery.Method.COURIER and address.strip():
            addr=DeliveryAddress.objects.create(user=order.user,address=address.strip())
            return Delivery.objects.create(order=order,method=method,delivery_address=addr)
        raise ValueError('Укажите способ и адрес получения')
    @staticmethod
    @transaction.atomic
    def change_status(delivery,status):
        transitions={Delivery.Status.NEW:{Delivery.Status.READY},Delivery.Status.READY:{Delivery.Status.OUT,Delivery.Status.DELIVERED},Delivery.Status.OUT:{Delivery.Status.DELIVERED}}
        d=Delivery.objects.select_for_update().get(pk=delivery.pk)
        if status not in transitions.get(d.status,set()): raise ValueError('Недопустимый статус доставки')
        d.status=status;d.save(update_fields=['status']);return d
