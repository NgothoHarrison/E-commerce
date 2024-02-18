from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse


def cart_summary(request):
    # get the cart
    cart = Cart(request)
   
    # get the context
    cart_products = cart.get_prods() # get the products
    quantities = cart.get_quants()
    return render(request, 'cart_summary.html', {"cart_products": cart_products, "quantities": quantities})

def cart_add(request):
    # Get the cart
    cart = Cart(request)
    # Test the post
    if request.POST.get('action') == 'post':
        # Get the product id
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty')) # get the quantity

        # Look up the product in database
        product = get_object_or_404(Product, id=product_id)

        # save to the session
        cart.add(product=product, quantity=product_qty)
        # return the response

        # get cart quantity
        cart_quantity = cart.__len__()

        # response = JsonResponse({'Product name ': product.name})
        response = JsonResponse({'qty': cart_quantity})
        return response

# def cart_delete(request):
#     return redirect('cart_summary')

# def cart_update(request):
#     return redirect('cart_summary')