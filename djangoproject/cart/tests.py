# cart/tests.py

from django.test import TestCase, Client
from django.urls import reverse
from shop_webapp.models import Product

class CartTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.product = Product.objects.create(
            name="Test Product",
            price=100.00,
        )
        from .cart import Cart  # Імпортуємо тут, щоб уникнути кругового імпорту
        self.cart = Cart(self.client)

    def test_cart_summary_view(self):
        response = self.client.get(reverse('cart_summary'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart_summary.html')

    def test_cart_add_view(self):
        response = self.client.post(reverse('cart_add'), {'action': 'post', 'product_id': self.product.id})
        self.assertEqual(response.status_code, 200)
        expected_response = {
            'Product Name': self.product.name,
            'Discounted Price': str(format(self.product.get_discounted_price(), '.2f'))
        }
        self.assertJSONEqual(response.content, expected_response)

    def test_cart_delete_view(self):
        self.cart.add(self.product)
        response = self.client.post(reverse('cart_delete'), {'action': 'post', 'product_id': self.product.id})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'product': self.product.id})

    def test_cart_update_view(self):
        pass

    def test_cart_add(self):
        self.cart.add(self.product)
        self.assertIn(str(self.product.id), self.cart.cart)
        self.assertEqual(self.cart.cart[str(self.product.id)]['price'], str(self.product.price))
        self.assertEqual(self.cart.cart[str(self.product.id)]['discounted_price'], str(self.product.get_discounted_price()))

    def test_cart_delete(self):
        self.cart.add(self.product)
        self.cart.delete(self.product.id)
        self.assertNotIn(str(self.product.id), self.cart.cart)

    def test_get_prods(self):
        self.cart.add(self.product)
        products = self.cart.get_prods()
        self.assertIn(self.product, products)
        self.assertEqual(products[0].get_discounted_price(), self.product.get_discounted_price())

    def test_cart_empty(self):
        self.assertEqual(len(self.cart.cart), 0)

    def test_cart_add_multiple_products(self):
        product2 = Product.objects.create(
            name="Test Product 2",
            price=150.00,
        )
        self.cart.add(self.product)
        self.cart.add(product2)
        self.assertIn(str(self.product.id), self.cart.cart)
        self.assertIn(str(product2.id), self.cart.cart)
        self.assertEqual(len(self.cart.cart), 2)

    def test_cart_clear(self):
        self.cart.add(self.product)
        self.cart.clear()
        self.assertEqual(len(self.cart.cart), 1)

    def test_cart_add_same_product_twice(self):
        self.cart.add(self.product)
        self.cart.add(self.product)
        self.assertEqual(len(self.cart.cart), 1)
        self.assertEqual(self.cart.cart[str(self.product.id)]['price'], str(self.product.price))
        self.assertEqual(self.cart.cart[str(self.product.id)]['discounted_price'], str(self.product.get_discounted_price()))
