from decimal import Decimal
from django.db import transaction
from .models import Cart,CartItem
from catalog.models import Product

class CartService:
    @staticmethod
    def get_cart(user):
        if not user.is_authenticated: raise ValueError('Войдите в аккаунт')
        return Cart.objects.get_or_create(user=user)[0]
    @classmethod
    @transaction.atomic
    def add_item(cls,user,product_id,quantity=1):
        if quantity<=0: raise ValueError('Количество должно быть положительным')
        product=Product.objects.get(pk=product_id,is_active=True,is_available=True)
        cart=cls.get_cart(user)
        item,created=CartItem.objects.get_or_create(cart=cart,product=product,defaults={'quantity':quantity})
        if not created: item.quantity+=quantity; item.save(update_fields=['quantity'])
        return item
    @staticmethod
    def update_quantity(user,product_id,quantity):
        if quantity<=0: raise ValueError('Количество должно быть положительным')
        item=CartItem.objects.get(cart__user=user,product_id=product_id)
        item.quantity=quantity; item.save(update_fields=['quantity']); return item
    @staticmethod
    def remove_item(user,product_id): CartItem.objects.filter(cart__user=user,product_id=product_id).delete()
    @staticmethod
    def clear(user): CartItem.objects.filter(cart__user=user).delete()
    @staticmethod
    def calculate_total(cart):
        return sum((item.product.price*item.quantity for item in cart.items.select_related('product')),Decimal('0.00'))
