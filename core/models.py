from django.db import models


class Testimonial(models.Model):
    guest_name = models.CharField(max_length=120)
    location = models.CharField(max_length=100, blank=True)
    rating = models.PositiveSmallIntegerField(default=5)
    comment = models.TextField()
    room_stayed = models.CharField(max_length=120, blank=True)
    stay_date = models.DateField()
    is_featured = models.BooleanField(default=True)

    class Meta:
        ordering = ['-stay_date']

    def __str__(self):
        return f"{self.guest_name} ({self.rating}★)"

    @property
    def stars_range(self):
        return range(self.rating)


class ContactInquiry(models.Model):
    SUBJECT_CHOICES = [
        ('booking', 'Booking Question'),
        ('events', 'Events & Conferences'),
        ('feedback', 'Feedback'),
        ('partnership', 'Partnership / Corporate'),
        ('other', 'Other'),
    ]
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    subject = models.CharField(max_length=20, choices=SUBJECT_CHOICES, default='other')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Contact inquiries'

    def __str__(self):
        return f"{self.name} - {self.subject}"
