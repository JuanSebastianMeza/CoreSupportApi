from django.urls import path

from .views import get_subscribers_data


urlpatterns = [
    path('', get_subscribers_data, name='get_subscribers_data'),
]