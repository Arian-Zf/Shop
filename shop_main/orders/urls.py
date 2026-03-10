from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('verify-form', views.verify_form, name='verify_form'),
    path('verify-code', views.verify_code, name='verify_code'),

]