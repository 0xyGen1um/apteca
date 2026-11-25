from django.urls import path
from . import views
app_name='prescriptions'
urlpatterns=[path('',views.queue,name='queue')]
