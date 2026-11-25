from django.urls import path
from . import views
app_name='orders'
urlpatterns=[path('checkout/',views.checkout,name='checkout'),path('manage/',views.manage,name='manage'),path('<int:pk>/',views.detail,name='detail'),path('<int:pk>/cancel/',views.cancel,name='cancel')]
