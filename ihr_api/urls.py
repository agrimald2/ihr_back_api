from django.urls import path, include
from rest_framework import routers
from ihr_api import views
from rest_framework_simplejwt import views as jwt_views
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register(r'product', views.ProductViewSet)
router.register(r'category', views.CategoryViewSet)
router.register(r'subcategory', views.SubcategoryViewSet)
router.register(r'store', views.StoreViewSet)
router.register(r'country', views.CountryViewSet)
router.register(r'currency', views.CurrencyViewSet)
router.register(r'sale', views.SaleViewSet)
router.register(r'payment', views.PaymentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.APITokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.CreateUserView.as_view(), name='create_user'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
