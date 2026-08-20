from django.urls import path
from . import views

app_name = 'amenities'

urlpatterns = [
    path('', views.amenity_list, name='list'),
]
