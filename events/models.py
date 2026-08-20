from django.db import models


class EventSpace(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField()
    capacity_seated = models.PositiveIntegerField()
    capacity_standing = models.PositiveIntegerField()
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='events/')
    features = models.TextField(help_text='Comma separated, e.g. Stage, PA System, Projector')

    def __str__(self):
        return self.name

    @property
    def features_list(self):
        return [f.strip() for f in self.features.split(',') if f.strip()]


class EventInquiry(models.Model):
    EVENT_TYPE_CHOICES = [
        ('wedding', 'Wedding'),
        ('conference', 'Conference / Business Meeting'),
        ('birthday', 'Birthday / Anniversary'),
        ('corporate', 'Corporate Retreat'),
        ('other', 'Other'),
    ]
    STATUS_CHOICES = [
        ('new', 'New Inquiry'),
        ('quoted', 'Quote Sent'),
        ('confirmed', 'Confirmed'),
        ('closed', 'Closed'),
    ]
    reference_code = models.CharField(max_length=20, unique=True, editable=False, blank=True)
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES)
    event_space = models.ForeignKey(EventSpace, on_delete=models.SET_NULL, null=True, blank=True)
    preferred_date = models.DateField()
    guest_count = models.PositiveIntegerField()
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Event inquiries'

    def save(self, *args, **kwargs):
        if not self.reference_code:
            import random, string
            self.reference_code = 'EVT-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.reference_code} - {self.full_name}"
