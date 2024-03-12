from django.urls import path, include
from rest_framework import routers
from ihr_api import views
from rest_framework_simplejwt import views as jwt_views

router = routers.DefaultRouter()
router.register(r'product', views.ProductViewSet)
router.register(r'category', views.CategoryViewSet)
router.register(r'subcategory', views.SubcategoryViewSet)
router.register(r'store', views.StoreViewSet)
router.register(r'country', views.CountryViewSet)
router.register(r'currency', views.CurrencyViewSet)
router.register(r'sale', views.SaleViewSet)
router.register(r'payment', views.PaymentViewSet)
router.register(r'billing_account', views.BillingAccountViewSet)
router.register(r'payment_link', views.PaymentLinkViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.APITokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.CreateUserView.as_view(), name='create_user'),
    path('product/<int:id>/', views.ProductRetrieveAPIView.as_view(), name='product-detail'),
    path('crypto_confirmation/<str:sale_reference>/', views.crypto_confirm_callback, name='crypto_confirm_callback'),
    path('payment_link/retrieve/<str:sale_reference>/', views.payment_link_retrieve, name='payment_link_retrieve'),
]
