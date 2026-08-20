from django.contrib import admin
from .models import StaffProfile, ShiftSchedule

@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'phone')

@admin.register(ShiftSchedule)
class ShiftScheduleAdmin(admin.ModelAdmin):
    list_display = ('staff', 'date', 'shift')
