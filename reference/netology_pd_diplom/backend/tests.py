from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from rest_framework.test import RequestsClient
from backend.models import User, Order, Contact
from backend.views import ContactView

factory = APIRequestFactory()

request = factory.get('/api/v1/shops/')
print(request)
request = factory.put('/api/v1/user/register')
print(request)


user = User.objects.get(email='nailka9@mail.ru')
view = ContactView.as_view()

# Make an authenticated request to the view...
request = factory.get('/api/v1/user/contact')
force_authenticate(request, user=user, token=None)
response = view(request)
print(response)
request = factory.get('/api/v1/user/details')
force_authenticate(request, user=user, token=None)
response = view(request)
print(response)
request = factory.get('/api/v1/user/login')
force_authenticate(request, user=user, token=None)
response = view(request)
print(response)



client = RequestsClient()
response = client.get('http://testserver/api/v1/products')
force_authenticate(response, user=user, token=None)
assert response.status_code == 200
print(response)
response = client.get('http://testserver/api/v1/categories')
force_authenticate(response, user=user, token=None)
assert response.status_code == 200
print(response)

# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Order, ProductInfo, ProductParameter, Parameter, Product, Category, Shop
from .serializers import OrderSerializer


class BasketViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass', email='None')
        self.category = Category.objects.create(name='Test Category')
        self.shop = Shop.objects.create(name='Test Shop', state=True)
        self.product = Product.objects.create(name='Test Product', category=self.category)
        self.product_parameter = Parameter.objects.create(name='Test Parameter')
        self.product_info = ProductInfo.objects.create(product=self.product, shop=self.shop, price=100)
        self.product_info.product_parameters.add(self.product_parameter)
        self.order = Order.objects.create(user=self.user)

    def test_edit_basket_with_authenticated_user(self):
        url = reverse('basket')
        self.client.force_authenticate(user=self.user)

        # добавляем товар в корзину
        data = {
            'ordered_items': [
                {
                    'product_info': self.product_info.id,
                    'quantity': 2,
                    'parameters': [
                        {
                            'parameter': self.product_parameter.id,
                            'value': 'Test Value'
                        }
                    ]
                }
            ]
        }
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # проверяем, что товар добавлен в корзину
        order = Order.objects.get(id=self.order.id)
        self.assertEqual(order.ordered_items.count(), 1)
        ordered_item = order.ordered_items.first()
        self.assertEqual(ordered_item.product_info, self.product_info)
        self.assertEqual(ordered_item.quantity, 2)
        product_parameter = ordered_item.product_parameters.first()
        self.assertEqual(product_parameter.parameter, self.product_parameter)
        self.assertEqual(product_parameter.value, 'Test Value')

        # редактируем товар в корзине
        data = {
            'ordered_items': [
                {
                    'id': ordered_item.id,
                    'product_info': self.product_info.id,
                    'quantity': 3,
                    'parameters': [
                        {
                            'parameter': self.product_parameter.id,
                            'value': 'New Test Value'
                        }
                    ]
                }
            ]
        }
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # проверяем, что товар отредактирован в корзине
        order = Order.objects.get(id=self.order.id)
        self.assertEqual(order.ordered_items.count(), 1)
        ordered_item = order.ordered_items.first()
        self.assertEqual(ordered_item.product_info, self.product_info)
        self.assertEqual(ordered_item.quantity, 3)
        product_parameter = ordered_item.product_parameters.first()
        self.assertEqual(product_parameter.parameter, self.product_parameter)
        self.assertEqual(product_parameter.value, 'New Test Value')

    def test_edit_basket_with_unauthenticated_user(self):
        url = reverse('basket')

        # попытка редактирования корзины неавторизованным пользователем
        data = {
            'ordered_items': [
                {
                    'product_info': self.product_info.id,
                    'quantity': 2,
                    'parameters': [
                        {
                            'parameter': self.product_parameter.id,
                            'value': 'Test Value'
                        }
                    ]
                }
            ]
        }
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # проверяем, что корзина не изменилась
        order = Order.objects.get(id=self.order.id)
        self.assertEqual(order.ordered_items.count(), 0)

    def test_edit_basket_with_invalid_data(self):
        url = reverse('basket')
        self.client.force_authenticate(user=self.user)

        # попытка добавления товара в корзину с неверными данными
        data = {
            'ordered_items': [
                {
                    'product_info': self.product_info.id,
                    'quantity': 0,  # неверное количество
                    'parameters': [
                        {
                            'parameter': self.product_parameter.id,
                            'value': 'Test Value'
                        }
                    ]
                }
            ]
        }
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # проверяем, что корзина не изменилась
        order = Order.objects.get(id=self.order.id)
        self.assertEqual(order.ordered_items.count(), 0)

    def test_get_basket_with_authenticated_user(self):
        url = reverse('basket')
        self.client.force_authenticate(user=self.user)

        # получаем корзину
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # проверяем, что данные корзины верны
        order = Order.objects.get(id=self.order.id)
        serializer = OrderSerializer(order)
        self.assertEqual(response.data, serializer.data)

    def test_get_basket_with_unauthenticated_user(self):
        url = reverse('basket')

        # попытка получения корзины неавторизованным пользователем
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)