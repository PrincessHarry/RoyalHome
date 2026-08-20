from django.shortcuts import render, redirect
from django.contrib import messages
from rooms.models import RoomType
from restaurant.models import MenuItem
from amenities.models import Amenity
from events.models import EventSpace
from gallery.models import GalleryImage
from blog.models import BlogPost
from .models import Testimonial, ContactInquiry


def home(request):
    context = {
        'featured_rooms': RoomType.objects.filter(is_featured=True)[:3] or RoomType.objects.all()[:3],
        'amenities': Amenity.objects.filter(is_highlighted=True)[:6] or Amenity.objects.all()[:6],
        'event_spaces': EventSpace.objects.all()[:2],
        'signature_dishes': MenuItem.objects.filter(is_signature=True)[:4],
        'testimonials': Testimonial.objects.filter(is_featured=True)[:6],
        'gallery_preview': GalleryImage.objects.all()[:8],
        'blog_posts': BlogPost.objects.all()[:3],
    }
    return render(request, 'core/home.html', context)


def about(request):
    return render(request, 'core/about.html')


def contact(request):
    if request.method == 'POST':
        ContactInquiry.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            subject=request.POST.get('subject', 'other'),
            message=request.POST.get('message'),
        )
        messages.success(request, "Thank you! Your message has been received — our team will respond within 24 hours.")
        return redirect('core:contact')
    return render(request, 'core/contact.html')


def custom_404(request, exception):
    """Custom 404 handler."""
    return render(request, '404.html', status=404)


def custom_500(request):
    """Custom 500 handler."""
    return render(request, '500.html', status=500)
