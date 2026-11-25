from django.contrib import admin
from .models import PickupPoint,DeliveryAddress,Delivery
admin.site.register(PickupPoint)
admin.site.register(DeliveryAddress)
admin.site.register(Delivery)
