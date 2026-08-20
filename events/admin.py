from django.contrib import admin
from .models import EventSpace, EventInquiry

@admin.register(EventSpace)
class EventSpaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity_seated', 'capacity_standing', 'price_per_hour')

@admin.register(EventInquiry)
class EventInquiryAdmin(admin.ModelAdmin):
    list_display = ('reference_code', 'full_name', 'event_type', 'preferred_date', 'guest_count', 'status')
    list_filter = ('status', 'event_type')
