from django.urls import path
from .views import country_details_view

urlpatterns = [
    path('', country_details_view, name='country_details'),
    # path('about/', about_view, name='about'),
    # path('team/', team_view, name='team'),
]