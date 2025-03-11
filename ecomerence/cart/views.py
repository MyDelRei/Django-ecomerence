from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from store.models import Product
from .cart import Cart  
from decimal import Decimal

def cart_summary(request):
    cart = Cart(request)
    print("Cart object:", cart)
    print("self.cart:", cart.cart)
    print("Type of self.cart:", type(cart.cart))
    return render(request, 'cart/cart-summary.html', {'cart': cart})

def cart_add(request):
    cart = Cart(request)

    if request.method == 'POST': 
        print('post recieve')

        product_id = request.POST.get('product_id')
        product_quantity = request.POST.get('product_quantity')

        if product_id is None or product_quantity is None:
            return JsonResponse({'error': 'Missing product_id or product_quantity'}, status=400)

        try:
            product_id = str(product_id)
            product_quantity = int(product_quantity)
            print('post recieve 2')

            print('post recieve abpve 404')
            product = get_object_or_404(Product, id=product_id)
            print('post recieve 3')

            cart.add(product=product, product_qty=product_quantity)
            

            print(f"✅ Product {product.title} added to cart")  

            return JsonResponse({'qty': product_quantity})

        except ValueError:
            return JsonResponse({'error': 'Invalid product_id or product_quantity'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Unexpected error: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

def cart_delete(request):
    cart = Cart(request)
    print("Cart before delete:", cart.cart)
    if request.method == "POST" and request.POST.get('action') == 'post':
        try:
            product_id = int(request.POST.get('product_id'))
            print("Deleting product_id:", product_id)
            cart.delete(product=product_id)  # Fixed keyword argument
            print("Cart after delete:", cart.cart)
            cart_qty = cart.__len__()
            print("Cart quantity:", cart_qty)
            cart_total = cart.get_total()
            print("Cart total:", cart_total)
            response = JsonResponse({'qty': cart_qty, 'total': str(cart_total)})
            return response
        except ValueError:
            return JsonResponse({'error': 'Invalid product ID'}, status=400)
        except Exception as e:
            print("Exception in cart_delete:", str(e))
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)

from django.http import JsonResponse
from decimal import Decimal
from .cart import Cart

def cart_update(request):
    cart = Cart(request)
    print("1")
    print("above if")
    if request.method == "POST" and request.POST.get('action') == 'post':  # Match lowercase 'post'
        print("in if")
        try:
            product_id = int(request.POST.get('product_id'))
            print("2")
            print("product_qty from POST:", request.POST.get('product_qty'))  # Debug POST data
            product_qty = int(request.POST.get('product_qty'))
            print("3")
            cart.update(product_id=product_id, qty=product_qty)  # Match Cart.update
            cart_qty = cart.__len__()
            cart_total = cart.get_total()
            response = JsonResponse({'qty': cart_qty, 'total': str(cart_total)})
            return response
        except ValueError as e:
            print("ValueError:", str(e))
            return JsonResponse({'error': 'Invalid product ID or quantity'}, status=400)
        except Exception as e:
            print(f"Exception in cart_update: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)
    print("Invalid request or action")
    print("POST data:", request.POST)  # Debug full POST data
    return JsonResponse({'error': 'Invalid request or action'}, status=400)
        
