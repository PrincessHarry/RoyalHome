from django.urls import path
from . import views

app_name = 'guestportal'

urlpatterns = [
    path('', views.lookup, name='lookup'),
    path('<str:reference_code>/', views.dashboard, name='dashboard'),
    path('<str:reference_code>/order/', views.place_order, name='place_order'),
]
