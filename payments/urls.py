from django.urls import path
from . import views
app_name='payments'
urlpatterns=[path('<int:order_id>/',views.pay,name='pay')]
