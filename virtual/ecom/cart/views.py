from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product, Category
from django.http import JsonResponse
from django.contrib import messages

def cart_summary(request):
	# Get the cart
	cart = Cart(request)
	cart_products = cart.get_prods
	quantities = cart.get_quants

	totals = cart.cart_total() # Get the cart total

	return render(request, "cart_summary.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals})

def category_summary(request):
	categories = Category.objects.all()

	return render(request, "category_summary.html", {"categories":categories})



def cart_add(request):
	# Get the cart
	cart = Cart(request)
	# test for POST
	if request.POST.get('action') == 'post':
		# Get stuff
		product_id = int(request.POST.get('product_id'))
		product_qty = int(request.POST.get('product_qty'))

		# lookup product in DB
		product = get_object_or_404(Product, id=product_id)
		
		# Save to session
		cart.add(product=product, quantity=product_qty)

		# Get Cart Quantity
		cart_quantity = cart.__len__()

		# Return resonse
		# response = JsonResponse({'Product Name: ': product.name})
		response = JsonResponse({'qty': cart_quantity})
		messages.success(request, ("Product Added To Cart..."))
		return response
	

def cart_update(request):
	cart = Cart(request)
	if request.POST.get('action') == 'post':
		# get stuff
		product_id = int(request.POST.get('product_id'))
		product_qty = int(request.POST.get('product_qty'))
		# update cart
		cart.update(product=product_id, quantity=product_qty)
		# get cart quantity
		cart_qty = cart.__len__()
		# return response
		response = JsonResponse({'qty': cart_qty})
		return response
	
	
def cart_delete(request):
	cart = Cart(request)
	if request.POST.get('action') == 'post':
		# get stuff
		product_id = int(request.POST.get('product_id'))
		# delete from cart
		cart.delete(product=product_id)
		# get cart quantity
		
		# return response
		response = JsonResponse({'product': product_id})
		return response
