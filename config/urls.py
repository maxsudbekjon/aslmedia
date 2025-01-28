from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,)
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from config import settings

urlpatterns = [
       path('admin/', admin.site.urls),
    path('user/',include('user.urls')),
    path('film/',include('film.urls')),
    path('api-auth/', include('rest_framework.urls')),
path('api/schema/', SpectacularAPIView.as_view(), name='schema'),  # Schema generatsiyasi
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),  # Swagger UI
    path('api/docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # ReDoc
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
