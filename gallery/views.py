from django.shortcuts import render
from .models import GalleryImage


def gallery(request):
    images = GalleryImage.objects.all()
    category = request.GET.get('category')
    if category and category != 'all':
        images = images.filter(category=category)
    return render(request, 'gallery/gallery.html', {
        'images': images,
        'categories': GalleryImage.CATEGORY_CHOICES,
        'selected_category': category or 'all',
    })
