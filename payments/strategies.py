from abc import ABC,abstractmethod
from decimal import Decimal

class IPaymentMethod(ABC):
    @abstractmethod
    def pay(self,amount:Decimal,token:str): ...
    @abstractmethod
    def refund(self,amount:Decimal): ...

class CardPayment(IPaymentMethod):
    def __init__(self,last4='',card_brand=''):
        if last4 and (len(last4)!=4 or not last4.isdigit()): raise ValueError('Укажите только 4 последние цифры')
        self.last4=last4;self.card_brand=card_brand[:30]
    def pay(self,amount,token): return token!='decline'
    def refund(self,amount): return True

class SBPPayment(IPaymentMethod):
    def pay(self,amount,token): return token!='decline'
    def refund(self,amount): return True

class CashPayment(IPaymentMethod):
    def pay(self,amount,token): return True
    def refund(self,amount): return True
