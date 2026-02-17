from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from django.http import JsonResponse



@require_POST
def add_to_cart(request, product_id):
    try:
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.add(product)
        context = {
            'item_count': len(cart),
            'total_price':cart.get_total_price(),
        }
        return JsonResponse(context)
    except:
        return JsonResponse({'error': 'An error occurred while adding the product to the cart.'})

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})

@require_POST
def update_quantity(request):
    item_id = request.POST.get('item_id')
    action = request.POST.get('action')
    try:
        product = get_object_or_404(Product, id=item_id)
        cart = Cart(request)
        if action == 'increment':
            cart.add(product)
        elif action == 'decrement':
            cart.decrease(product)
        context = {
            'item_count': len(cart),
            'total_price':cart.get_total_price(),
            'success': True
        }

        return JsonResponse(context)
    except:
        return JsonResponse({'success':False,'error': 'An error occurred while updating the cart.'}) 
    

@require_POST
def remove_item(request):
    item_id = request.POST.get('item_id')
    try:
        product = get_object_or_404(Product, id=item_id)
        cart = Cart(request)
        cart.remove(product)
        
        return JsonResponse({
            'success': True,
            'item_count': len(cart),
            'total_price': cart.get_total_price()
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': 'An error occurred while updating the cart.'})

