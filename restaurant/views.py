from django.shortcuts import render
from .models import MenuCategory


def menu(request):
    categories = MenuCategory.objects.prefetch_related('items').all()
    return render(request, 'restaurant/menu.html', {'categories': categories})
