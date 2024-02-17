from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse


def cart_summary(request):
    return render(request, 'cart_summary.html', {})

def cart_add(request):
    # Get the cart
    cart = Cart(request)
    # Test the post
    if request.POST.get('action') == 'post':
        # Get the product id
        product_id = int(request.POST.get('product_id'))
        # Look up the product in database
        product = get_object_or_404(Product, id=product_id)
        # save to the session
        cart.add(product=product)
        # return the response

        # get cart quantity
        cart_quantity = cart.__len__()

        # response = JsonResponse({'Product name ': product.name})
        response = JsonResponse({'qty ': cart_quantity })
        return response

# def cart_delete(request):
#     return redirect('cart_summary')

# def cart_update(request):
#     return redirect('cart_summary')