from datetime import datetime
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from rooms.models import RoomType
from .models import Booking, AddOn


def book(request):
    rooms = RoomType.objects.all()
    addons = AddOn.objects.all()

    preselected_room = request.GET.get('room')

    if request.method == 'POST':
        room_id = request.POST.get('room_type')
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')
        adults = int(request.POST.get('adults', 1))
        children = int(request.POST.get('children', 0))
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        special_requests = request.POST.get('special_requests', '')
        selected_addons = request.POST.getlist('addons')
        payment_method = request.POST.get('payment_method', 'Paystack')

        room = get_object_or_404(RoomType, id=room_id)
        ci = datetime.strptime(check_in, '%Y-%m-%d').date()
        co = datetime.strptime(check_out, '%Y-%m-%d').date()
        nights = max(1, (co - ci).days)

        room_total = room.base_price * nights
        addon_qs = AddOn.objects.filter(id__in=selected_addons)
        addon_total = sum([a.price for a in addon_qs], Decimal('0'))
        grand_total = room_total + addon_total

        booking = Booking.objects.create(
            room_type=room,
            check_in=ci,
            check_out=co,
            adults=adults,
            children=children,
            full_name=full_name,
            email=email,
            phone=phone,
            special_requests=special_requests,
            room_total=room_total,
            addon_total=addon_total,
            grand_total=grand_total,
            payment_method=payment_method,
            status='confirmed',
            payment_status='paid' if payment_method == 'Paystack' else 'partial',
        )
        booking.addons.set(addon_qs)
        messages.success(request, 'Booking confirmed! A confirmation has been sent to your email and WhatsApp.')
        return redirect('bookings:confirmation', reference_code=booking.reference_code)

    return render(request, 'bookings/book.html', {
        'rooms': rooms,
        'addons': addons,
        'preselected_room': preselected_room,
    })


def confirmation(request, reference_code):
    booking = get_object_or_404(Booking, reference_code=reference_code)
    return render(request, 'bookings/confirmation.html', {'booking': booking})


def manage_lookup(request):
    if request.method == 'POST':
        ref = request.POST.get('reference_code', '').strip().upper()
        email = request.POST.get('email', '').strip().lower()
        try:
            booking = Booking.objects.get(reference_code=ref, email__iexact=email)
            return redirect('bookings:manage_detail', reference_code=booking.reference_code)
        except Booking.DoesNotExist:
            messages.error(request, "We couldn't find a booking with that reference and email. Please double-check and try again.")
    return render(request, 'bookings/manage_lookup.html')


def manage_detail(request, reference_code):
    booking = get_object_or_404(Booking, reference_code=reference_code)
    return render(request, 'bookings/manage_detail.html', {'booking': booking})


def cancel_booking(request, reference_code):
    booking = get_object_or_404(Booking, reference_code=reference_code)
    if request.method == 'POST':
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, 'Your booking has been cancelled. A refund (if applicable) will be processed within 5-7 business days.')
    return redirect('bookings:manage_detail', reference_code=reference_code)
