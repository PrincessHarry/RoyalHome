import random
import string
from django.db import models
from django.urls import reverse
from rooms.models import RoomType


def generate_reference():
    return 'XPH-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))


class AddOn(models.Model):
    name = models.CharField(max_length=120)
    description = models.CharField(max_length=255, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    icon = models.CharField(max_length=40, default='sparkles')

    def __str__(self):
        return self.name


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Payment'),
        ('confirmed', 'Confirmed'),
        ('checked_in', 'Checked In'),
        ('checked_out', 'Checked Out'),
        ('cancelled', 'Cancelled'),
    ]
    PAYMENT_CHOICES = [
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid'),
        ('partial', 'Partial (Pay at Hotel)'),
    ]

    reference_code = models.CharField(max_length=20, unique=True, default=generate_reference, editable=False)
    room_type = models.ForeignKey(RoomType, on_delete=models.PROTECT, related_name='bookings')
    check_in = models.DateField()
    check_out = models.DateField()
    adults = models.PositiveIntegerField(default=1)
    children = models.PositiveIntegerField(default=0)

    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    whatsapp_opt_in = models.BooleanField(default=True)
    special_requests = models.TextField(blank=True)

    addons = models.ManyToManyField(AddOn, blank=True, related_name='bookings')

    room_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    addon_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    grand_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='unpaid')
    payment_method = models.CharField(max_length=40, default='Paystack')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.reference_code} - {self.full_name}"

    def get_absolute_url(self):
        return reverse('bookings:confirmation', args=[self.reference_code])

    @property
    def nights(self):
        return max(1, (self.check_out - self.check_in).days)
