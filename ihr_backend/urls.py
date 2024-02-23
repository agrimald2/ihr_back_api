from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', admin.site.urls),
    path('api/', include('ihr_api.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
