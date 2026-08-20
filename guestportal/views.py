from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from bookings.models import Booking
from restaurant.models import MenuItem
from .models import ServiceOrder


def lookup(request):
    if request.method == 'POST':
        ref = request.POST.get('reference_code', '').strip().upper()
        if Booking.objects.filter(reference_code=ref).exists():
            return redirect('guestportal:dashboard', reference_code=ref)
        messages.error(request, "We couldn't find that reference code. Please check your confirmation email or SMS.")
    return render(request, 'guestportal/lookup.html')


def dashboard(request, reference_code):
    booking = get_object_or_404(Booking, reference_code=reference_code)
    orders = booking.service_orders.all()
    menu_items = MenuItem.objects.filter(is_available_room_service=True)[:12]
    return render(request, 'guestportal/dashboard.html', {
        'booking': booking,
        'orders': orders,
        'menu_items': menu_items,
    })


def place_order(request, reference_code):
    booking = get_object_or_404(Booking, reference_code=reference_code)
    if request.method == 'POST':
        order_type = request.POST.get('order_type')
        details = request.POST.get('details')
        amount = request.POST.get('amount') or 0
        payment_option = request.POST.get('payment_option', 'charge_to_room')
        ServiceOrder.objects.create(
            booking=booking,
            order_type=order_type,
            details=details,
            amount=amount,
            payment_option=payment_option,
        )
        messages.success(request, 'Your request has been sent! Track its status below.')
    return redirect('guestportal:dashboard', reference_code=reference_code)
