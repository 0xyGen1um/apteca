from django import forms
from enums import PaymentMethodType
from delivery.models import Delivery,PickupPoint

class CheckoutForm(forms.Form):
    payment_method=forms.ChoiceField(choices=PaymentMethodType.choices,label='Оплата')
    delivery_method=forms.ChoiceField(choices=Delivery.Method.choices,label='Получение')
    pickup_point=forms.ModelChoiceField(queryset=PickupPoint.objects.filter(is_active=True),required=False,label='Пункт выдачи')
    address=forms.CharField(required=False,label='Адрес курьера')
    comment=forms.CharField(required=False,widget=forms.Textarea(attrs={'rows':2}),label='Комментарий')
    prescription_image=forms.ImageField(required=False,label='Фото рецепта')
