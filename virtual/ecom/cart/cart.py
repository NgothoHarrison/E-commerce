from store.models import Product


class Cart():
    def __init__(self, request):
        self.session = request.session

        # Get the current session if the key exists, 
        cart = self.session.get('session_key')

        # If the key does not exist, create a new session
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        # make sure that cart is available on all pages
        self.cart = cart

    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)

        if product_id in self.cart:
            pass
        # if product_id not in self.cart:
        #     self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        # if update_quantity:
        #     self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]= int(product_qty) # add the quantity
            # self.cart[product_id]= { 'price ': str(product.price)}
           
            # self.cart[product_id] = {'price': str(product.price)}

        self.session.modified = True


    def __len__(self):
        return len(self.cart)
        # return sum(item['quantity'] for item in self.cart.values())
    

    def get_prods(self):
        product_ids = self.cart.keys() # Get the product ids
        # use ids to get products in database model
        products = Product.objects.filter(id__in=product_ids)
        return products
    
    def get_quants(self):
        quantities = self.cart
        return quantities
    
    def update(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)

        self.cart[product_id] = product_qty
        self.session.modified = True

    def delete(self, product):
        product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True



    # def save(self):
    #     self.session[settings.CART_SESSION_ID] = self.cart
    #     self.session.modified = True

    # def remove(self, product):
    #     product_id = str(product.id)
    #     if product_id in self.cart:
    #         del self.cart[product_id]
    #         self.save()

    # def __iter__(self):
    #     product_ids = self.cart.keys()
    #     products = Product.objects.filter(id__in=product_ids)
    #     for product in products:
    #         self.cart[str(product.id)]['product'] = product

    #     for item in self.cart.values():
    #         item['price'] = Decimal(item['price'])
    #         item['total_price'] = item['price'] * item['quantity']
    #         yield item

    

    # def get_total_price(self):
    #     return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    # def clear(self):
    #     del self.session[settings.CART_SESSION_ID]
    #     self.session.modified = True