from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('', include('core.urls')),
    path('rooms/', include('rooms.urls')),
    path('book/', include('bookings.urls')),
    path('restaurant/', include('restaurant.urls')),
    path('amenities/', include('amenities.urls')),
    path('events/', include('events.urls')),
    path('gallery/', include('gallery.urls')),
    path('blog/', include('blog.urls')),
    path('my-stay/', include('guestportal.urls')),
    path('staff/', include('dashboard.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / 'static')

# Custom error handlers
handler404 = 'core.views.custom_404'
handler500 = 'core.views.custom_500'
