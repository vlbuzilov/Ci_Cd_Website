from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages

from .models import Profile, Product
from .forms import UserInfoForm


class ProfileModelTest(TestCase):
    """
    Test suite for the Profile model.
    """

    def setUp(self):
        """
        Set up initial data for the tests.
        Create a User instance, which should automatically create a Profile instance.
        """
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.profile = Profile.objects.get(user=self.user)

    def test_profile_creation(self):
        """
        Test that a Profile is automatically created when a User is created.
        """
        self.assertIsInstance(self.profile, Profile)
        self.assertEqual(self.profile.user, self.user)

    def test_profile_str(self):
        """
        Test the __str__ method of the Profile model.
        """
        self.assertEqual(str(self.profile), self.user.username)

    def test_profile_fields(self):
        """
        Test the fields of the Profile model.
        """
        self.profile.phone = '1234567890'
        self.profile.address1 = '123 Main St'
        self.profile.address2 = 'Apt 4'
        self.profile.city = 'Springfield'
        self.profile.state = 'IL'
        self.profile.country = 'USA'
        self.profile.zipcode = '62701'
        self.profile.save()

        profile = Profile.objects.get(user=self.user)
        self.assertEqual(profile.phone, '1234567890')
        self.assertEqual(profile.address1, '123 Main St')
        self.assertEqual(profile.address2, 'Apt 4')
        self.assertEqual(profile.city, 'Springfield')
        self.assertEqual(profile.state, 'IL')
        self.assertEqual(profile.country, 'USA')
        self.assertEqual(profile.zipcode, '62701')

    def test_profile_update(self):
        """
        Test updating the fields of the Profile model.
        """
        self.profile.phone = '0987654321'
        self.profile.city = 'New City'
        self.profile.save()

        profile = Profile.objects.get(user=self.user)
        self.assertEqual(profile.phone, '0987654321')
        self.assertEqual(profile.city, 'New City')

    def test_profile_deletion(self):
        """
        Test that deleting a User instance also deletes the associated Profile instance.
        """
        user_id = self.user.id
        self.user.delete()
        self.assertFalse(Profile.objects.filter(user_id=user_id).exists())

    def test_profile_invalid_phone(self):
        """
        Test validation for an invalid phone number.
        """
        self.profile.address1 = '123 Main St'
        self.profile.address2 = 'Apt 4'
        self.profile.city = 'Springfield'
        self.profile.state = 'IL'
        self.profile.country = 'USA'
        self.profile.zipcode = '62701'
        self.profile.phone = 'invalid_phone_number_000000000000000'
        with self.assertRaises(ValidationError):
            self.profile.full_clean()

    def test_profile_default_values(self):
        """
        Test default values of the Profile model fields.
        """
        self.profile.delete()
        profile = Profile.objects.create(
            user=self.user,
            address1='Default Address 1',
            address2='Default Address 2',
            city='Default City',
            state='Default State',
            country='Default Country',
            zipcode='00000'
        )
        self.assertEqual(profile.phone, '')
        self.assertEqual(profile.address1, 'Default Address 1')
        self.assertEqual(profile.address2, 'Default Address 2')
        self.assertEqual(profile.city, 'Default City')
        self.assertEqual(profile.state, 'Default State')
        self.assertEqual(profile.country, 'Default Country')
        self.assertEqual(profile.zipcode, '00000')


class UpdateInfoViewTestSecond(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client = Client()
        self.client.login(username='testuser', password='12345')

    def test_update_info_view_GET(self):
        response = self.client.get(reverse('update_info'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'update_info.html')

    def test_update_info_view_POST(self):
        response = self.client.post(reverse('update_info'), {
            'phone': '1234567890',
            'address1': '123 Main St',
            'address2': 'Apt 4',
            'city': 'Springfield',
            'state': 'IL',
            'country': 'USA',
            'zipcode': '62701'
        })
        self.assertEqual(response.status_code, 200)


class LogoutUserViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client = Client()
        self.client.login(username='testuser', password='12345')

    def test_logout_user_view(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('home'))
        storage = get_messages(response.wsgi_request)
        self.assertEqual(list(storage)[0].tags, 'success')
        self.assertEqual(str(list(storage)[0]), "You have been logged out")


class UpdateInfoViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client = Client()
        self.client.login(username='testuser', password='12345')

    def test_update_info_view_POST(self):
        response = self.client.post(reverse('update_info'), {
            'phone': '1234567890',
            'address1': '123 Main St',
            'address2': 'Apt 4',
            'city': 'Springfield',
            'state': 'IL',
            'country': 'USA',
            'zipcode': '62701'
        })
        self.assertEqual(response.status_code, 200)


class UserInfoFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com',
                                             first_name='John', last_name='Doe', password='12345')
        self.profile = self.user.profile

    def test_form_fields(self):
        form = UserInfoForm(user=self.user)
        self.assertTrue('username' in form.fields)
        self.assertTrue('email' in form.fields)
        self.assertTrue('first_name' in form.fields)
        self.assertTrue('last_name' in form.fields)
        self.assertTrue('phone' in form.fields)
        self.assertTrue('address1' in form.fields)
        self.assertTrue('address2' in form.fields)
        self.assertTrue('city' in form.fields)
        self.assertTrue('state' in form.fields)
        self.assertTrue('country' in form.fields)
        self.assertTrue('zipcode' in form.fields)

    def test_save_method(self):
        form = UserInfoForm(user=self.user, data={
            'username': 'newusername',
            'email': 'newemail@example.com',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'phone': '1234567890',
            'address1': '123 New St',
            'address2': 'Apt 5',
            'city': 'New City',
            'state': 'NY',
            'country': 'USA',
            'zipcode': '10001'
        }, instance=self.profile)
        self.assertTrue(form.is_valid())
        form.save()
        updated_user = User.objects.get(pk=self.user.id)
        updated_profile = updated_user.profile
        self.assertEqual(updated_user.username, 'newusername')
        self.assertEqual(updated_user.email, 'newemail@example.com')
        self.assertEqual(updated_user.first_name, 'Jane')
        self.assertEqual(updated_user.last_name, 'Smith')
        self.assertEqual(updated_profile.phone, '1234567890')
        self.assertEqual(updated_profile.address1, '123 New St')
        self.assertEqual(updated_profile.address2, 'Apt 5')
        self.assertEqual(updated_profile.city, 'New City')
        self.assertEqual(updated_profile.state, 'NY')
        self.assertEqual(updated_profile.country, 'USA')
        self.assertEqual(updated_profile.zipcode, '10001')
class ProductModelTest(TestCase):
    """
    Test suite for the Product model.
    """

    def setUp(self):
        self.sample_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'\x00\x00\x00\x00',
            content_type='image/jpeg'
        )
        self.product = Product.objects.create(
            type='phone',
            name='Test Phone',
            price=999.99,
            description='A sample description.',
            image=self.sample_image,
            discount=10.00,
            color='black',
            isDiscount=True
        )

    def test_product_creation(self):
        """
        Test that a product is created correctly.
        """
        product = self.product
        self.assertIsInstance(product, Product)
        self.assertEqual(product.type, 'phone')
        self.assertEqual(product.name, 'Test Phone')
        self.assertEqual(product.price, 999.99)
        self.assertEqual(product.description, 'A sample description.')
        self.assertEqual(product.discount, 10.00)
        self.assertEqual(product.color, 'black')
        self.assertTrue(product.isDiscount)

    def test_default_values(self):
        """
        Test that default values are set correctly.
        """
        product = Product.objects.create(
            name='Default Test Product',
            price=499.99,
            description='A sample description.',
            image=self.sample_image,
        )
        self.assertEqual(product.type, 'phone')
        self.assertEqual(product.color, 'white')
        self.assertFalse(product.isDiscount)

    def test_get_discounted_price(self):
        """
        Test the get_discounted_price method.
        """
        product = self.product
        discounted_price = product.get_discounted_price()
        self.assertEqual(discounted_price, 899.991)

    def test_get_discounted_price_no_discount(self):
        """
        Test the get_discounted_price method when there is no discount.
        """
        product = Product.objects.create(
            name='No Discount Product',
            price=499.99,
            description='A sample description.',
            image=self.sample_image,
        )
        self.assertEqual(product.get_discounted_price(), 499.99)

    def test_product_str(self):
        """
        Test the __str__ method of the Product model.
        """
        product = self.product
        self.assertEqual(str(product), 'Test Phone')

    def test_invalid_discount_value(self):
        """
        Test that an invalid discount value raises a ValidationError.
        """
        with self.assertRaises(ValidationError):
            product_invalid = Product(
                name='Invalid Discount Product',
                price=499.99,
                description='A sample description.',
                image=self.sample_image,
                discount=-5.00,
            )
            product_invalid.full_clean()  # This will trigger the validation
            product_invalid.save()

    def test_invalid_price_value(self):
        """
        Test that an invalid price value raises a ValidationError.
        """
        with self.assertRaises(ValidationError):
            product_invalid = Product(
                name='Invalid Price Product',
                price=-100.00,
                description='A sample description.',
                image=self.sample_image,
            )
            product_invalid.full_clean()  # This will trigger the validation
            product_invalid.save()
    def test_max_length_name(self):
        """
        Test the maximum length constraint of the name field.
        """
        product = Product.objects.create(
            name='A' * 30,
            price=499.99,
            description='A sample description.',
            image=self.sample_image,
        )
        self.assertEqual(len(product.name), 30)

    def test_max_length_type(self):
        """
        Test the maximum length constraint of the type field.
        """
        product = Product.objects.create(
            type='A' * 20,
            name='Test Product',
            price=499.99,
            description='A sample description.',
            image=self.sample_image,
        )
        self.assertEqual(len(product.type), 20)

    def test_max_length_color(self):
        """
        Test the maximum length constraint of the color field.
        """
        product = Product.objects.create(
            name='Test Product',
            price=499.99,
            description='A sample description.',
            image=self.sample_image,
            color='A' * 20,
        )
        self.assertEqual(len(product.color), 20)

    def test_discounted_price_rounding(self):
        """
        Test that the discounted price is rounded correctly.
        """
        product = Product.objects.create(
            name='Rounded Discount Product',
            price=100.00,
            description='A sample description.',
            image=self.sample_image,
            discount=33.33,
            isDiscount=True
        )
        self.assertAlmostEqual(product.get_discounted_price(), 66.67, places=2)

    def test_discount_with_no_isDiscount(self):
        """
        Test that discount is not applied if isDiscount is False.
        """
        product = Product.objects.create(
            name='Non Discounted Product',
            price=100.00,
            description='A sample description.',
            image=self.sample_image,
            discount=20.00,
            isDiscount=False,
        )
        self.assertEqual(product.get_discounted_price(), 100.00)

    def test_discount_greater_than_100(self):
        """
        Test that a discount greater than 100 is not allowed.
        """
        product_invalid = Product(
            name='Excessive Discount Product',
            price=100.00,
            description='A sample description.',
            image=self.sample_image,
            discount=150.00,
        )
        try:
            product_invalid.full_clean()  # This will trigger the validation
        except ValidationError as e:
            self.assertIn('discount', e.message_dict)
            self.assertIn('Ensure this value is less than or equal to 100.', e.message_dict['discount'])

    def test_blank_description(self):
        """
        Test that a blank description is allowed.
        """
        product = Product.objects.create(
            name='No Description Product',
            price=100.00,
            image=self.sample_image,
        )
        self.assertEqual(product.description, '')

    def test_null_discount(self):
        """
        Test that a null discount value is allowed and defaults correctly.
        """
        product = Product.objects.create(
            name='No Discount Product',
            price=100.00,
            description='A sample description.',
            image=self.sample_image,
            discount=None,
        )
        self.assertIsNone(product.discount)

    def test_product_choices(self):
        """
        Test that only valid product choices are allowed.
        """
        product = Product.objects.create(
            type='laptop',
            name='Laptop Product',
            price=1000.00,
            description='A sample description.',
            image=self.sample_image,
        )
        self.assertEqual(product.type, 'laptop')

        with self.assertRaises(ValidationError):
            product_invalid = Product(
                type='invalid_choice',
                name='Invalid Choice Product',
                price=100.00,
                description='A sample description.',
                image=self.sample_image,
            )
            product_invalid.full_clean()  # This will trigger the validation
            product_invalid.save()  # This is not reached if validation fails