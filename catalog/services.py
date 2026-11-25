from django.db import transaction
from .models import Inventory

class InventoryService:
    @staticmethod
    def check(product, quantity):
        return quantity > 0 and Inventory.objects.filter(product=product,stock_quantity__gte=quantity).exists()
    @staticmethod
    @transaction.atomic
    def write_off(product, quantity):
        stock=Inventory.objects.select_for_update().get(product=product)
        if quantity<=0 or stock.stock_quantity<quantity: raise ValueError('Недостаточно товара на складе')
        stock.stock_quantity-=quantity; stock.save(update_fields=['stock_quantity'])
    @staticmethod
    @transaction.atomic
    def restore(product, quantity):
        if quantity<=0: raise ValueError('Количество должно быть положительным')
        stock=Inventory.objects.select_for_update().get(product=product)
        stock.stock_quantity+=quantity; stock.save(update_fields=['stock_quantity'])
