from django.shortcuts import render, get_object_or_404
from .models import RoomType


def room_list(request):
    rooms = RoomType.objects.all()
    category = request.GET.get('category')
    guests = request.GET.get('guests')
    max_price = request.GET.get('max_price')

    if category and category != 'all':
        rooms = rooms.filter(category=category)
    if guests:
        rooms = rooms.filter(capacity_adults__gte=guests)
    if max_price:
        rooms = rooms.filter(base_price__lte=max_price)

    context = {
        'rooms': rooms,
        'categories': RoomType.CATEGORY_CHOICES,
        'selected_category': category or 'all',
    }
    return render(request, 'rooms/list.html', context)


def room_detail(request, slug):
    room = get_object_or_404(RoomType, slug=slug)
    related = RoomType.objects.exclude(id=room.id)[:3]
    return render(request, 'rooms/detail.html', {'room': room, 'related': related})
