from store.models import Product, Profile


class Cart():
    def __init__(self, request):
        self.session = request.session
        # Get request session
        self.request = request

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

        # deal with logged in users
        if self.request.user.is_authenticated:
            # get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # Convert Json format to string
            cartString = str(self.cart)
            cartString = cartString.replace("'", "\"")
            # save the new cart to Profile
            current_user.update(old_cart=cartString)


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

    def cart_total(self):
        product_ids = self.cart.keys() # Get the product ids
        # use ids to get products in database model
        products = Product.objects.filter(id__in=product_ids)

        quantities = self.cart 
        total = 0 # Set the total to zero

        for key, value in quantities.items():
            key = int(key)
            for product in products:
                if product.id == key:
                    total = total + (product.price * int(value))

        formatted_total = "{:,.2f}".format(total)

        return formatted_total

# Function to add items to the cart in session
    def db_add(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)

        if product_id in self.cart:
            pass
        
        else:
            self.cart[product_id]= int(product_qty) # add the quantity
            
        self.session.modified = True

        # deal with logged in users
        if self.request.user.is_authenticated:
            # get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # Convert Json format to string
            cartString = str(self.cart)
            cartString = cartString.replace("'", "\"")
            # save the new cart to Profile
            current_user.update(old_cart=cartString)