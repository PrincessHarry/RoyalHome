from django.db import models
from bookings.models import Booking


class ServiceOrder(models.Model):
    TYPE_CHOICES = [
        ('food', 'Room Service - Food & Drinks'),
        ('laundry', 'Laundry'),
        ('housekeeping', 'Housekeeping'),
        ('extra', 'Extras (Airport Pickup, Spa, Late Checkout, Wake-up Call)'),
    ]
    STATUS_CHOICES = [
        ('new', 'New'),
        ('acknowledged', 'Acknowledged'),
        ('in_progress', 'In Progress'),
        ('ready', 'Ready / Done'),
        ('delivered', 'Delivered'),
    ]
    PAYMENT_CHOICES = [
        ('charge_to_room', 'Charge to Room'),
        ('pay_instantly', 'Pay Instantly'),
    ]

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='service_orders')
    order_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    details = models.TextField(help_text='Free text summary of the order, e.g. "2x Jollof Rice, 1x Towels"')
    room_number = models.CharField(max_length=10, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_option = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='charge_to_room')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    placed_via = models.CharField(max_length=30, default='Guest Portal')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_order_type_display()} for {self.booking.reference_code}"

    STATUS_STEPS = ['new', 'acknowledged', 'in_progress', 'ready', 'delivered']

    @property
    def progress_percent(self):
        try:
            idx = self.STATUS_STEPS.index(self.status)
        except ValueError:
            idx = 0
        return int((idx / (len(self.STATUS_STEPS) - 1)) * 100)
