from django.contrib import admin
from .models import Testimonial, ContactInquiry

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('guest_name', 'rating', 'room_stayed', 'stay_date', 'is_featured')

@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'email', 'created_at')
    list_filter = ('subject',)
