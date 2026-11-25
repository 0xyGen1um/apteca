from django.db import models

class UserRole(models.TextChoices):
    USER = 'USER', 'Клиент'
    PHARMACIST = 'PHARMACIST', 'Фармацевт'
    ADMIN = 'ADMIN', 'Администратор'
    COURIER = 'COURIER', 'Курьер'

class PrescriptionStatus(models.TextChoices):
    PENDING = 'PENDING', 'На проверке'
    APPROVED = 'APPROVED', 'Одобрен'
    REJECTED = 'REJECTED', 'Отклонён'

class OrderStatus(models.TextChoices):
    NEW = 'NEW', 'Новый'
    AWAITING_PRESCRIPTION = 'AWAITING_PRESCRIPTION', 'Ожидает рецепт'
    PAID = 'PAID', 'Оплачен'
    READY = 'READY', 'Готов'
    OUT_FOR_DELIVERY = 'OUT_FOR_DELIVERY', 'В доставке'
    DELIVERED = 'DELIVERED', 'Доставлен'
    COMPLETED = 'COMPLETED', 'Завершён'
    CANCELLED = 'CANCELLED', 'Отменён'

ORDER_TRANSITIONS = {
    OrderStatus.NEW: {OrderStatus.AWAITING_PRESCRIPTION, OrderStatus.PAID, OrderStatus.CANCELLED},
    OrderStatus.AWAITING_PRESCRIPTION: {OrderStatus.NEW, OrderStatus.CANCELLED},
    OrderStatus.PAID: {OrderStatus.READY, OrderStatus.OUT_FOR_DELIVERY, OrderStatus.CANCELLED},
    OrderStatus.READY: {OrderStatus.COMPLETED, OrderStatus.CANCELLED},
    OrderStatus.OUT_FOR_DELIVERY: {OrderStatus.DELIVERED, OrderStatus.CANCELLED},
    OrderStatus.DELIVERED: {OrderStatus.COMPLETED},
    OrderStatus.COMPLETED: set(), OrderStatus.CANCELLED: set(),
}

class PaymentMethodType(models.TextChoices):
    CARD = 'CARD', 'Карта'
    SBP = 'SBP', 'СБП'
    CASH = 'CASH', 'Наличные'

class PaymentStatus(models.TextChoices):
    PENDING = 'PENDING', 'Ожидание'
    SUCCESS = 'SUCCESS', 'Успех'
    FAILED = 'FAILED', 'Отказ'
    REFUNDED = 'REFUNDED', 'Возврат'
