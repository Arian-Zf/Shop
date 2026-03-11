from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('verify-form', views.verify_phone, name='verify_form'),
    path('verify-code', views.verify_code, name='verify_code'),

]