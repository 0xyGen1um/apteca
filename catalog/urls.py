from django.urls import path
from . import views
app_name='catalog'
urlpatterns=[path('',views.home,name='home'),path('products/<int:pk>/',views.product,name='product')]
