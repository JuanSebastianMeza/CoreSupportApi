# Django imports
from django.contrib import admin
from django.urls import path, include

# JWT rest framework imports
from rest_framework_jwt.views import refresh_jwt_token
from authentication.views import obtain_jwt_token

# Rest framework imports
from rest_framework.routers import DefaultRouter

# Own imports
from authentication.views import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
	# Admin panel
    path('admin/', admin.site.urls),
    # JWT auth
    path('get-auth-token/', obtain_jwt_token),
    path('api-token-refresh/', refresh_jwt_token),
    # Router for views
    path('api/', include(router.urls)),
]
