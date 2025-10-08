from django.urls import path
from .views import GetSubscribersData


urlpatterns = [
    path('', GetSubscribersData.as_view(), name='get_subscribers_data'),
]