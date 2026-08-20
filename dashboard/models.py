from django.db import models
from django.contrib.auth.models import User


class StaffProfile(models.Model):
    ROLE_CHOICES = [
        ('super_admin', 'Super Admin'),
        ('front_desk', 'Front Desk'),
        ('kitchen', 'Kitchen'),
        ('laundry', 'Laundry'),
        ('housekeeping', 'Housekeeping'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff_profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.get_role_display()})"


class ShiftSchedule(models.Model):
    SHIFT_CHOICES = [
        ('morning', 'Morning (6am - 2pm)'),
        ('afternoon', 'Afternoon (2pm - 10pm)'),
        ('night', 'Night (10pm - 6am)'),
    ]
    staff = models.ForeignKey(StaffProfile, on_delete=models.CASCADE, related_name='shifts')
    date = models.DateField()
    shift = models.CharField(max_length=20, choices=SHIFT_CHOICES)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f"{self.staff} - {self.date} ({self.shift})"
