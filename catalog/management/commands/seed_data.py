from decimal import Decimal
from datetime import date
from django.core.management.base import BaseCommand
from accounts.models import User
from catalog.models import Category,Product,Inventory
from delivery.models import PickupPoint
from orders.models import Order,OrderItem
from enums import UserRole,OrderStatus,PaymentMethodType

DATA={
 'Боль и температура':['Парацетамол','Ибупрофен','Аспирин','Нурофен'],
 'Простуда и грипп':['Терафлю','Фервекс','Лазолван','Амброксол'],
 'Витамины':['Витамин C','Витамин D3','Магний B6','Компливит'],
 'Пищеварение':['Смекта','Энтеросгель','Омепразол','Мезим'],
 'Антибиотики и рецептурные':['Амоксициллин','Азитромицин','Цефиксим','Доксициклин'],
}
class Command(BaseCommand):
    help='Создаёт демонстрационные данные аптеки'
    def handle(self,*args,**options):
        users={}
        for role,email in [(UserRole.USER,'client@example.com'),(UserRole.PHARMACIST,'pharmacist@example.com'),(UserRole.COURIER,'courier@example.com'),(UserRole.ADMIN,'admin@example.com')]:
            user,created=User.objects.get_or_create(email=email,defaults={'user_name':role.title(),'role':role,'birth_date':date(1990,1,1),'is_staff':role==UserRole.ADMIN,'is_superuser':role==UserRole.ADMIN})
            if created: user.set_password('Demo12345!');user.save()
            users[role]=user
        products=[]
        for index,(category_name,names) in enumerate(DATA.items()):
            category,_=Category.objects.get_or_create(name=category_name,defaults={'description':'Лекарства и товары для здоровья'})
            for offset,name in enumerate(names):
                product,_=Product.objects.get_or_create(name=name,defaults={'category':category,'description':f'{name}. Перед применением прочитайте инструкцию и проконсультируйтесь со специалистом.','price':Decimal(99+index*80+offset*35),'requires_prescription':index==4,'age_limit':18 if index==4 or name in ('Аспирин','Терафлю') else 0})
                Inventory.objects.get_or_create(product=product,defaults={'stock_quantity':25+offset*5})
                products.append(product)
        for name,address in [('Центральная аптека','ул. Центральная, 1'),('Аптека у парка','ул. Парковая, 12')]: PickupPoint.objects.get_or_create(name=name,defaults={'address':address})
        client=users[UserRole.USER]
        for status,product in [(OrderStatus.NEW,products[0]),(OrderStatus.PAID,products[1]),(OrderStatus.COMPLETED,products[2])]:
            order,created=Order.objects.get_or_create(user=client,status=status,comment='Демонстрационный заказ',defaults={'total_amount':product.price,'payment_method':PaymentMethodType.CARD,'stock_written_off':status!=OrderStatus.NEW})
            if created: OrderItem.objects.create(order=order,product=product,quantity=1,unit_price=product.price)
        self.stdout.write(self.style.SUCCESS('Готово: 4 пользователя, 5 категорий, 20 товаров, 2 пункта выдачи, 3 заказа. Пароль демо: Demo12345!'))
