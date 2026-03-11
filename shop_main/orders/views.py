from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import PhoneVerificationForm
from  account.models import ShopUser
import random
from django.contrib.auth import login



def verify_form(request):
    if request.method == 'POST':
        pass
    else:
        form = PhoneVerificationForm()

    return render(request, 'verify_form.html',{'form':form})
