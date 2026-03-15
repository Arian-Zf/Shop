from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import PhoneVerificationForm
from  account.models import ShopUser
import random
from django.contrib.auth import login
from .forms import OrderCreateForm, OrderItem
# from cart.common.KaveSms import send_sms_with_template
from cart.cart import Cart 
from django.contrib.auth.decorators import login_required



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
            return redirect('shop:product_list')
    else:
        form = OrderCreateForm()

    return render(request, 'order_create.html', {'form': form, 'cart': cart})



from django.conf import settings
import requests
import json

# بررسی محیط تست (سندباکس) یا محیط واقعی
# اگر متغیر SANDBOX در settings.py برابر با True باشد، درگاه در حالت تست کار می‌کند
if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'

# آدرس‌های پایه‌ای ای‌پی‌آی (API) زرین‌پال بر اساس محیط تست یا واقعی
ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"

# اطلاعات اولیه برای ایجاد تراکنش
amount = 1000  # مبلغ تراکنش (به تومان یا ریال بستگی به تنظیمات درگاه شما دارد) - الزامی
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # الزامی
phone = 'YOUR_PHONE_NUMBER'  # شماره تلفن کاربر - اختیاری

# آدرس بازگشت کاربر پس از انجام پرداخت در درگاه بانکی
# نکته مهم: این آدرس باید برای سرور واقعی (پروژه اصلی) تغییر کند و با آدرس سایت شما جایگزین شود.
CallbackURL = 'http://127.0.0.1:8000/verify/'



def send_request(request):
    # آماده‌سازی اطلاعات برای ارسال به زرین‌پال
    data = {
        "MerchantID": settings.MERCHANT,  # کد مرچنت شما که در settings.py قرار دارد
        "Amount": amount,                 # مبلغ (از متغیرهای تعریف شده در بخش قبل)
        "Description": description,       # توضیحات تراکنش
        "Phone": phone,                   # شماره تماس خریدار
        "CallbackURL": CallbackURL,       # آدرس بازگشت پس از پرداخت
    }
    
    # تبدیل دیکشنری پایتون به فرمت JSON
    data = json.dumps(data)
    
    # تنظیم هدرها (Headers) برای ارسال درخواست
    headers = {
        'content-type': 'application/json',
        'content-length': str(len(data))
    }
    
    try:
        # ارسال درخواست POST به سرور زرین‌پال
        response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)
        
        # اگر ارتباط با سرور موفقیت‌آمیز بود (کد 200)
        if response.status_code == 200:
            response_data = response.json()
            
            # در نسخه وب‌گیت زرین‌پال، کد 100 به معنای تایید اولیه و موفقیت است
            if response_data['Status'] == 100:
                return {
                    'status': True, 
                    'url': ZP_API_STARTPAY + str(response_data['Authority']),
                    'authority': response_data['Authority']
                }
            else:
                # اگر زرین‌پال خطایی برگرداند (مثلا مبلغ نامعتبر بود یا مرچنت اشتباه بود)
                return {
                    'status': False, 
                    'code': str(response_data['Status'])
                }
        return response

    except requests.exceptions.Timeout:
        return {'status': False,'code': 'timeout'}
    except requests.exceptions.ConnectionError:
        return {'status': False,'code': 'connection error'}

def verify(authority):
    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": amount,
        "Authority": authority,
    }
    
    data = json.dumps(data)
    
    # set content length by data
    headers = {
        'content-type': 'application/json',
        'content-length': str(len(data))
    }
    
    response = requests.post(ZP_API_VERIFY, data=data, headers=headers)
    
    if response.status_code == 200:
        response = response.json()
        if response['Status'] == 100:
            return {'status': True, 'RefID': response['RefID']}
        else:
            return {'status': False, 'code': str(response['Status'])}
            
    return response
