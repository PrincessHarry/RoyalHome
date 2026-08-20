from django.db import models


class Amenity(models.Model):
    CATEGORY_CHOICES = [
        ('wellness', 'Wellness & Recreation'),
        ('business', 'Business & Events'),
        ('convenience', 'Convenience'),
        ('safety', 'Safety & Trust'),
    ]
    name = models.CharField(max_length=120)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='wellness')
    description = models.TextField()
    icon = models.CharField(max_length=40, default='sparkles', help_text='lucide icon name')
    image = models.ImageField(upload_to='amenities/', blank=True, null=True)
    hours = models.CharField(max_length=100, blank=True)
    is_highlighted = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Amenities'

    def __str__(self):
        return self.name
