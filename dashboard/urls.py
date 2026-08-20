from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('login/', views.staff_login, name='login'),
    path('logout/', views.staff_logout, name='logout'),
    path('admin/', views.super_admin, name='super_admin'),
    path('front-desk/', views.front_desk, name='front_desk'),
    path('kitchen/', views.kitchen, name='kitchen'),
    path('laundry/', views.laundry, name='laundry'),
    path('housekeeping/', views.housekeeping, name='housekeeping'),
    path('order/<int:order_id>/status/', views.update_order_status, name='update_order_status'),
    path('booking/<int:booking_id>/status/', views.update_booking_status, name='update_booking_status'),
]
