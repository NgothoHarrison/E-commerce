from .cart import Cart

# create context processor to make cart available to all templates

def cart(request):
    return {'cart': Cart(request)} #return the default data from the cart