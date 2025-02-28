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
from rest_framework_jwt.views import refresh_jwt_token
from authentication.views import (obtain_jwt_token, UserViewSet,
                                  WebAppsViewSet, WebAppModulesViewSet,
                                  GrantedAccessAuditViewSet, DeniedAccessAuditViewSet,
                                  AppAuditViewSet)


# Create reouter
ROUTER = DefaultRouter()
ROUTER.register(r'users', UserViewSet)
ROUTER.register(r'web-apps', WebAppsViewSet)
ROUTER.register(r'web-app-modules', WebAppModulesViewSet)


urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),
    # JWT auth
    path('get-auth-token/', obtain_jwt_token),
    path('api-token-refresh/', refresh_jwt_token),
    # Router for views
    path('api/', include(ROUTER.urls)),
    path('api/granted-access-audit/', GrantedAccessAuditViewSet.as_view()),
    path('api/denied-access-audit/', DeniedAccessAuditViewSet.as_view()),
    path('api/app-audit/', AppAuditViewSet.as_view()),
    path('docs/', TemplateView.as_view(template_name="index.html")),
]
