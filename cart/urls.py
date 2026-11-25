from django.urls import path
from . import views
app_name='cart'
urlpatterns=[path('',views.detail,name='detail'),path('item/<int:product_id>/',views.change,name='change')]
