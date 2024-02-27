from django.urls import path, include
from rest_framework import routers
from ihr_api import views
from rest_framework_simplejwt import views as jwt_views

router = routers.DefaultRouter()
router.register(r'product', views.ProductViewSet)
router.register(r'category', views.CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.APITokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.CreateUserView.as_view(), name='create_user'),
]
