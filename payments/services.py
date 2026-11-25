from uuid import uuid4
from django.db import transaction
from django.utils import timezone
from enums import PaymentMethodType,PaymentStatus,OrderStatus
from orders.models import Order
from catalog.services import InventoryService
from .models import Payment
from .strategies import CardPayment,SBPPayment,CashPayment

class PaymentService:
    @staticmethod
    @transaction.atomic
    def pay(order,outcome='success',transaction_id=None,last4='',card_brand=''):
        order=Order.objects.select_for_update().get(pk=order.pk)
        if order.status!=OrderStatus.NEW: raise ValueError('Заказ не готов к оплате')
        if transaction_id and Payment.objects.filter(transaction_id=transaction_id).exists():
            payment=Payment.objects.get(transaction_id=transaction_id)
            if payment.order_id!=order.pk: raise ValueError('Идентификатор операции занят')
            return payment
        if order.payments.count()>=3: raise ValueError('Превышено число попыток оплаты')
        strategy={PaymentMethodType.CARD:CardPayment(last4,card_brand),PaymentMethodType.SBP:SBPPayment(),PaymentMethodType.CASH:CashPayment()}[order.payment_method]
        payment=Payment.objects.create(order=order,amount=order.total_amount,method=order.payment_method,transaction_id=transaction_id or uuid4().hex,last4=getattr(strategy,'last4',''),card_brand=getattr(strategy,'card_brand',''))
        if outcome=='timeout': return payment
        if outcome=='decline' or not strategy.pay(order.total_amount,outcome):
            payment.status=PaymentStatus.FAILED
        elif outcome=='success':
            if not order.stock_written_off:
                for item in order.items.select_related('product'): InventoryService.write_off(item.product,item.quantity)
                order.stock_written_off=True
            order.status=OrderStatus.PAID;order.save(update_fields=['status','stock_written_off'])
            payment.status=PaymentStatus.SUCCESS
        else: raise ValueError('Неизвестный результат')
        payment.completed_at=timezone.now();payment.save(update_fields=['status','completed_at'])
        return payment
    @staticmethod
    @transaction.atomic
    def refund(order):
        payment=Payment.objects.select_for_update().filter(order=order,status=PaymentStatus.SUCCESS).first()
        if not payment: return None
        strategy={PaymentMethodType.CARD:CardPayment(),PaymentMethodType.SBP:SBPPayment(),PaymentMethodType.CASH:CashPayment()}[payment.method]
        if not strategy.refund(payment.amount): raise ValueError('Возврат не выполнен')
        payment.status=PaymentStatus.REFUNDED;payment.save(update_fields=['status'])
        return payment
