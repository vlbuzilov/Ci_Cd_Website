from shop_webapp.models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session

        cart = self.session.get("session_key")

        if "session_key" not in request.session:
            cart = self.session["session_key"] = {}

        self.cart = cart

    def add(self, product):
        product_id = str(product.id)
        discounted_price = product.get_discounted_price()

        if product_id in self.cart:
            # Update the product price and discounted price
            self.cart[product_id]['price'] = str(product.price)
            self.cart[product_id]['discounted_price'] = str(discounted_price)
        else:
            self.cart[product_id] = {'price': str(product.price), 'discounted_price': str(discounted_price)}

        self.session.modified = True

    def get_prods(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        for product in products:
            product_id = str(product.id)
            if 'discounted_price' not in self.cart[product_id]:
                self.cart[product_id]['discounted_price'] = str(product.get_discounted_price())
            product.discounted_price = self.cart[product_id]['discounted_price']

        return products

    def delete(self, product):
        product_id = str(product)

        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True
