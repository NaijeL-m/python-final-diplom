from django.urls import path, include
from django.conf.urls import url
from django_rest_passwordreset.views import reset_password_request_token, reset_password_confirm
from django.views.generic import TemplateView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from backend.views import PartnerUpdate, RegisterAccount, LoginAccount, CategoryView, ProductInfoView, \
    BasketView, AccountDetails, ContactView, OrderView, PartnerState, PartnerOrders, ConfirmAccount, ShopViewSet

schema_view = get_schema_view(
    openapi.Info(
        #  add your swagger doc title
        title="Showroom API",
        #  version of the swagger doc
        default_version='v1',
        # first line that appears on the top of the doc
        description="Test description",
    ),
    public=True,
)

url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui')

app_name = 'backend'
shop_list = ShopViewSet.as_view({
    'get': 'list',
    'put': 'create',
    'delete': 'destroy'
})
urlpatterns = [
    path('partner/update', PartnerUpdate.as_view(), name='partner-update'),
    path('partner/state', PartnerState.as_view(), name='partner-state'),
    path('partner/orders', PartnerOrders.as_view(), name='partner-orders'),
    path('user/register', RegisterAccount.as_view(), name='user-register'),
    path('user/register/confirm', ConfirmAccount.as_view(), name='user-register-confirm'),
    path('user/details', AccountDetails.as_view(), name='user-details'),
    path('user/contact', ContactView.as_view(), name='user-contact'),
    path('user/login', LoginAccount.as_view(), name='user-login'),
    path('user/password_reset', reset_password_request_token, name='password-reset'),
    path('user/password_reset/confirm', reset_password_confirm, name='password-reset-confirm'),
    path('categories', CategoryView.as_view(), name='categories'),
    path('shops/', shop_list, name='shops'),
    path('products', ProductInfoView.as_view(), name='shops'),
    path('basket', BasketView.as_view(), name='basket'),
    path('order', OrderView.as_view(), name='order'),
]
