from django.urls import path
from .views import country_details_view

urlpatterns = [
    path('', country_details_view, name='country_details'),
]