from django.db import models


class GalleryImage(models.Model):
    CATEGORY_CHOICES = [
        ('exterior', 'Exterior'),
        ('rooms', 'Rooms & Suites'),
        ('restaurant', 'Restaurant & Dining'),
        ('events', 'Events & Conference'),
        ('pool', 'Pool & Recreation'),
        ('spa', 'Spa & Wellness'),
    ]
    title = models.CharField(max_length=150)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='gallery/')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title
