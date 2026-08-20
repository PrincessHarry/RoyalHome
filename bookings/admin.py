from django.contrib import admin
from .models import Booking, AddOn

@admin.register(AddOn)
class AddOnAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('reference_code', 'full_name', 'room_type', 'check_in', 'check_out', 'status', 'payment_status', 'grand_total')
    list_filter = ('status', 'payment_status', 'room_type')
    search_fields = ('reference_code', 'full_name', 'email', 'phone')
