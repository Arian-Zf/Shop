from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import PhoneVerificationForm
from account.models import ShopUser
import random
from django.contrib.auth import login
from .forms import OrderCreateForm
# from cart.common.KaveSms import send_sms_with_template
from cart.cart import Cart 
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse
from .models import Order, OrderItem

# اضافه شدن کتابخانه‌های داخلی پایتون به جای requests
import urllib.request
import urllib.error
import json
import socket


def verify_phone(request):
    
    if request.user.is_authenticated:
        return redirect('orders:order_create')
    
    if request.method == 'POST':
        form = PhoneVerificationForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            if ShopUser.objects.filter(phone=phone).exists():
                messages.error(request, 'this phone is already registered.')
                return redirect('orders:verify_phone')
            else:
                tokens = {'token': ''.join(random.choices('0123456789', k=6))}
                request.session['verification_code'] = tokens['token']
                request.session['phone'] = phone
                print(tokens)
                # send_sms_with_template(phone, tokens, 'verify')
                messages.success(request, 'verificatio code send successfully ')
                return redirect('orders:order_create')
    else:
        form = PhoneVerificationForm()

    return render(request, 'verify_phone.html', {'form': form})


def verify_code(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        if code:
            verification_code = request.session['verification_code']
            phone = request.session['phone']
            if code == verification_code:
                user = ShopUser.objects.create_user(phone=phone,)
                user.set_password('123456')
                user.save()
                # send sms
                print(user)
                login(request, user)
                del request.session['verification_code']
                del request.session['phone']
                return redirect('shop:product_list')
            else:
                messages.error(request, 'Verification code is incorrect.')

    return render(request, 'verify_code.html')

    
@login_required
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            order.buyer=request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'],
                    weight=item['weight'],
                )
            cart.clear()
            request.session['order_id'] = order.id
            return redirect('orders:request')
    else:
        form = OrderCreateForm()

    return render(request, 'order_create.html', {'form': form, 'cart': cart})


if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'


ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"


CallbackURL = 'http://127.0.0.1:8000/order/verify/'


# تغییرات اصلی در این تابع انجام شد
def send_request(request):
    order = Order.objects.get(id=request.session['order_id'])
    description = ""
    for item in order.items.all():
        description += item.product.name + ", "
        
    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": order.get_final_cost(),
        "Description": description,
        "Phone": request.user.phone,
        "CallbackURL": CallbackURL,
    }
    
    # تبدیل داده‌ها به بایت برای ارسال با urllib
    data_json = json.dumps(data).encode('utf-8')
    
    headers = {
        'accept': 'application/json', 
        'content-type': 'application/json', 
        'content-length': str(len(data_json))
    }
    
    try:
        req = urllib.request.Request(ZP_API_REQUEST, data=data_json, headers=headers, method='POST')
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.getcode() == 200:
                response_data = response.read().decode('utf-8')
                response_json = json.loads(response_data)
                authority = response_json['Authority']
                
                if response_json['Status'] == 100:
                    return redirect(ZP_API_STARTPAY + authority)
                else:
                    return HttpResponse('Error')
                    
            return HttpResponse('response failed')
            
    except urllib.error.URLError as e:
        if isinstance(e.reason, socket.timeout):
            return HttpResponse('Timeout Error')
        return HttpResponse('Connection Error')
    except socket.timeout:
        return HttpResponse('Timeout Error')


# تغییرات اصلی در این تابع انجام شد
def verify(request):
    order = Order.objects.get(id=request.session['order_id'])
    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": order.get_final_cost(),
        "Authority": request.GET.get('Authority'),
    }
    
    # تبدیل داده‌ها به بایت برای ارسال با urllib
    data_json = json.dumps(data).encode('utf-8') 

    headers = {
        'accept': 'application/json', 
        'content-type': 'application/json', 
        'content-length': str(len(data_json))
    }
    
    try:
        req = urllib.request.Request(ZP_API_VERIFY, data=data_json, headers=headers, method='POST')
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.getcode() == 200:
                response_data = response.read().decode('utf-8')
                response_json = json.loads(response_data)
                reference_id = response_json['RefID']
                
                if response_json['Status'] == 100:
                    for item in order.items.all():
                        item.product.inventory -= item.quantity
                        item.product.save()
                    order.paid = True
                    order.save()
                    return render(request, 'payment-tracking.html', {'success': True, 'RefID': reference_id, 'order_id': order.id})
                else:
                    return render(request, 'payment-tracking.html', {'success': False})

            return HttpResponse('response failed')
            
    except urllib.error.URLError as e:
        if isinstance(e.reason, socket.timeout):
            return HttpResponse('Timeout Error')
        return HttpResponse('Connection Error')
    except socket.timeout:
        return HttpResponse('Timeout Error')


def orders_list(request):
    user = request.user
    orders = Order.objects.filter(buyer=user)
    return render(request, 'orders-list.html', {'orders': orders,})
