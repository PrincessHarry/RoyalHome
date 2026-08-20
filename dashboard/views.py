from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Sum, Q
from django.utils import timezone

from bookings.models import Booking
from guestportal.models import ServiceOrder
from events.models import EventInquiry
from core.models import ContactInquiry, Testimonial
from .models import StaffProfile, ShiftSchedule


ROLE_REDIRECT = {
    'super_admin': 'dashboard:super_admin',
    'front_desk': 'dashboard:front_desk',
    'kitchen': 'dashboard:kitchen',
    'laundry': 'dashboard:laundry',
    'housekeeping': 'dashboard:housekeeping',
}


def staff_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            try:
                role = user.staff_profile.role
            except StaffProfile.DoesNotExist:
                role = 'front_desk' if user.is_staff else None
            if user.is_superuser and not role:
                role = 'super_admin'
            return redirect(ROLE_REDIRECT.get(role, 'dashboard:front_desk'))
        messages.error(request, 'Invalid credentials. Please try again.')
    return render(request, 'dashboard/login.html')


def staff_logout(request):
    logout(request)
    return redirect('dashboard:login')


@login_required(login_url='dashboard:login')
def super_admin(request):
    bookings = Booking.objects.all()[:10]
    stats = {
        'total_bookings': Booking.objects.count(),
        'revenue': Booking.objects.filter(payment_status='paid').aggregate(t=Sum('grand_total'))['t'] or 0,
        'occupied_rooms': Booking.objects.filter(status__in=['confirmed', 'checked_in']).count(),
        'pending_orders': ServiceOrder.objects.exclude(status='delivered').count(),
        'event_inquiries': EventInquiry.objects.filter(status='new').count(),
        'new_messages': ContactInquiry.objects.count(),
    }
    orders_by_type = ServiceOrder.objects.values('order_type').annotate(count=Count('id'))
    recent_reviews = Testimonial.objects.all()[:5]
    staff = StaffProfile.objects.select_related('user').all()
    return render(request, 'dashboard/super_admin.html', {
        'bookings': bookings, 'stats': stats, 'orders_by_type': orders_by_type,
        'recent_reviews': recent_reviews, 'staff': staff,
    })


@login_required(login_url='dashboard:login')
def front_desk(request):
    today = timezone.localdate()
    arrivals = Booking.objects.filter(check_in=today).exclude(status='cancelled')
    departures = Booking.objects.filter(check_out=today).exclude(status='cancelled')
    in_house = Booking.objects.filter(status='checked_in')
    all_bookings = Booking.objects.all()[:20]
    return render(request, 'dashboard/front_desk.html', {
        'arrivals': arrivals, 'departures': departures, 'in_house': in_house, 'all_bookings': all_bookings,
    })


@login_required(login_url='dashboard:login')
def kitchen(request):
    orders = ServiceOrder.objects.filter(order_type='food').exclude(status='delivered')
    completed = ServiceOrder.objects.filter(order_type='food', status='delivered')[:10]
    return render(request, 'dashboard/kitchen.html', {'orders': orders, 'completed': completed})


@login_required(login_url='dashboard:login')
def laundry(request):
    orders = ServiceOrder.objects.filter(order_type='laundry').exclude(status='delivered')
    completed = ServiceOrder.objects.filter(order_type='laundry', status='delivered')[:10]
    return render(request, 'dashboard/laundry.html', {'orders': orders, 'completed': completed})


@login_required(login_url='dashboard:login')
def housekeeping(request):
    orders = ServiceOrder.objects.filter(order_type__in=['housekeeping', 'extra']).exclude(status='delivered')
    completed = ServiceOrder.objects.filter(order_type__in=['housekeeping', 'extra'], status='delivered')[:10]
    return render(request, 'dashboard/housekeeping.html', {'orders': orders, 'completed': completed})


@login_required(login_url='dashboard:login')
def update_order_status(request, order_id):
    order = get_object_or_404(ServiceOrder, id=order_id)
    if request.method == 'POST':
        next_status = request.POST.get('status')
        if next_status in dict(ServiceOrder.STATUS_CHOICES):
            order.status = next_status
            order.save()
    return redirect(request.META.get('HTTP_REFERER', 'dashboard:super_admin'))


@login_required(login_url='dashboard:login')
def update_booking_status(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        next_status = request.POST.get('status')
        if next_status in dict(Booking.STATUS_CHOICES):
            booking.status = next_status
            booking.save()
    return redirect(request.META.get('HTTP_REFERER', 'dashboard:front_desk'))
