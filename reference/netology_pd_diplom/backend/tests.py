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
