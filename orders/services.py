from decimal import Decimal
from django.db import transaction
from enums import OrderStatus,ORDER_TRANSITIONS,PaymentMethodType
from catalog.services import InventoryService
from cart.services import CartService
from .models import Order,OrderItem

class OrderService:
    @staticmethod
    @transaction.atomic
    def create_from_cart(user,payment_method,delivery_method,address='',pickup_point_id=None,prescription_image=None,comment=''):
        cart=CartService.get_cart(user)
        items=list(cart.items.select_related('product'))
        if not items: raise ValueError('Корзина пуста')
        if payment_method not in PaymentMethodType.values: raise ValueError('Неизвестный способ оплаты')
        total=Decimal('0.00');needs_rx=False
        for item in items:
            p=item.product
            if not p.is_active or not p.is_available or not InventoryService.check(p,item.quantity): raise ValueError(f'{p.name}: нет в наличии')
            if p.age_limit and (user.get_age() is None or user.get_age()<p.age_limit): raise ValueError(f'{p.name}: возрастное ограничение {p.age_limit}+')
            needs_rx|=p.requires_prescription
            total+=p.price*item.quantity
        if needs_rx and not prescription_image: raise ValueError('Загрузите фото рецепта')
        order=Order.objects.create(user=user,payment_method=payment_method,total_amount=total,address=address,comment=comment,status=OrderStatus.AWAITING_PRESCRIPTION if needs_rx else OrderStatus.NEW)
        for item in items: OrderItem.objects.create(order=order,product=item.product,quantity=item.quantity,unit_price=item.product.price)
        from delivery.services import DeliveryService
        DeliveryService.create(order,delivery_method,address,pickup_point_id)
        if needs_rx:
            from prescriptions.services import PrescriptionService
            for item in items:
                if item.product.requires_prescription: PrescriptionService.submit(order,item.product,prescription_image)
        CartService.clear(user)
        if payment_method==PaymentMethodType.CASH and not needs_rx:
            from payments.services import PaymentService
            PaymentService.pay(order)
        return order
    @staticmethod
    @transaction.atomic
    def change_status(order,status):
        o=Order.objects.select_for_update().get(pk=order.pk)
        if status==OrderStatus.PAID: raise ValueError('Статус оплаты меняется только через PaymentService')
        if status not in ORDER_TRANSITIONS.get(o.status,set()): raise ValueError('Недопустимый переход статуса')
        o.status=status;o.save(update_fields=['status']);return o
    @staticmethod
    @transaction.atomic
    def cancel(order):
        o=Order.objects.select_for_update().get(pk=order.pk)
        if o.status==OrderStatus.CANCELLED: return o
        if OrderStatus.CANCELLED not in ORDER_TRANSITIONS.get(o.status,set()): raise ValueError('Заказ нельзя отменить')
        if o.stock_written_off:
            for item in o.items.select_related('product'): InventoryService.restore(item.product,item.quantity)
            o.stock_written_off=False
        from payments.services import PaymentService
        PaymentService.refund(o)
        o.status=OrderStatus.CANCELLED;o.save(update_fields=['status','stock_written_off']);return o
