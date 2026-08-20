from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('', views.book, name='book'),
    path('confirmation/<str:reference_code>/', views.confirmation, name='confirmation'),
    path('manage/', views.manage_lookup, name='manage'),
    path('manage/<str:reference_code>/', views.manage_detail, name='manage_detail'),
    path('manage/<str:reference_code>/cancel/', views.cancel_booking, name='cancel'),
]
