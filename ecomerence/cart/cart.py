from django.db import models
from decimal import Decimal
from store.models import Product

# Create your models here.

from decimal import Decimal

class Cart:
    def __init__(self, request):
        self.session = request.session
        # Get existing cart from session, or initialize as empty dict if None
        cart = self.session.get('cart')  # Use 'cart' key, not 'session_key'
        if not isinstance(cart, dict):  # Ensure cart is a dictionary
            cart = self.session['cart'] = {}  # Initialize as empty dict
        self.cart = cart
    
    def add(self, product, product_qty):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]["qty"] = product_qty
        else:
            self.cart[product_id] = {'price': str(product.price), 'qty': product_qty}
        self.session['cart'] = self.cart  # Save under 'cart' key
        self.session.modified = True
    
    def __len__(self):
        return sum(item['qty'] for item in self.cart.values())

    def __iter__(self):
        all_products_id = self.cart.keys()
        products = Product.objects.filter(id__in=all_products_id)
        
        import copy
        cart = copy.deepcopy(self.cart)

        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total'] = item['price'] * item['qty']
            yield item
    def get_total(self):
        return sum(Decimal(item['price'])*item['qty'] for item in self.cart.values())

    def delete(self, product):
        product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]
        self.session.modified = True
    def update(self, product_id, qty):
        product_id = str(product_id)
        if product_id in self.cart:
            self.cart[product_id]['qty'] = qty
        self.session.modified = True
        