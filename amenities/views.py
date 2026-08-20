from django.shortcuts import render
from .models import Amenity


def amenity_list(request):
    amenities = Amenity.objects.all()
    return render(request, 'amenities/list.html', {'amenities': amenities})
