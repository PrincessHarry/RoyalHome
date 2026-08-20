from django.contrib import admin
from .models import ServiceOrder

@admin.register(ServiceOrder)
class ServiceOrderAdmin(admin.ModelAdmin):
    list_display = ('booking', 'order_type', 'status', 'amount', 'payment_option', 'created_at')
    list_filter = ('order_type', 'status')
