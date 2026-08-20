from django.shortcuts import render, redirect
from django.contrib import messages
from .models import EventSpace, EventInquiry


def event_list(request):
    spaces = EventSpace.objects.all()
    if request.method == 'POST':
        space_id = request.POST.get('event_space')
        inquiry = EventInquiry.objects.create(
            full_name=request.POST.get('full_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            event_type=request.POST.get('event_type'),
            event_space_id=space_id if space_id else None,
            preferred_date=request.POST.get('preferred_date'),
            guest_count=request.POST.get('guest_count') or 0,
            message=request.POST.get('message', ''),
        )
        messages.success(request, f"Thank you! Your inquiry ({inquiry.reference_code}) has been received. Our events team will send a custom quote within 24 hours.")
        return redirect('events:list')
    return render(request, 'events/list.html', {'spaces': spaces})
