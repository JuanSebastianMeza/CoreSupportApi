"""
Authentication related urls
"""
# Django imports
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
# Rest framework imports
from rest_framework.routers import DefaultRouter
# JWT rest framework imports
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from authentication.views import (CustomGetAuthTokenView, CustomTokenObtainPairView, UserViewSet, WebAppsViewSet, WebAppModulesViewSet, GrantedAccessAuditViewSet, DeniedAccessAuditViewSet, AppAuditViewSet)

# Create reouter
ROUTER = DefaultRouter()
ROUTER.register(r'users', UserViewSet)
ROUTER.register(r'web-apps', WebAppsViewSet)
ROUTER.register(r'web-app-modules', WebAppModulesViewSet)

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),
    # SIMPLE JWT auth
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('get-auth-token/', CustomGetAuthTokenView.as_view()),  # PRUEBA
    #subscriber data collector
    path('api/get-subscribers-data/', include('subscriber_data_collector.urls')),
    # Router for views
    path('api/', include(ROUTER.urls)),
    path('api/granted-access-audit/', GrantedAccessAuditViewSet.as_view()),
    path('api/denied-access-audit/', DeniedAccessAuditViewSet.as_view()),
    path('api/app-audit/', AppAuditViewSet.as_view()),
    path('docs/', TemplateView.as_view(template_name="index.html")),
]
