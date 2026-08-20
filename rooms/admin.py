from django.contrib import admin
from .models import RoomType, RoomImage

class RoomImageInline(admin.TabularInline):
    model = RoomImage
    extra = 1

@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'base_price', 'total_rooms', 'is_featured')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [RoomImageInline]
