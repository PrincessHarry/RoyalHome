from django.db import models
from django.urls import reverse


class RoomType(models.Model):
    CATEGORY_CHOICES = [
        ('standard', 'Standard'),
        ('deluxe', 'Deluxe'),
        ('exclusive', 'Exclusive Suite'),
        ('presidential', 'Presidential Suite'),
    ]

    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='standard')
    tagline = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2, help_text='Price per night in NGN')
    capacity_adults = models.PositiveIntegerField(default=2)
    capacity_children = models.PositiveIntegerField(default=1)
    bed_type = models.CharField(max_length=100, default='1 King Bed')
    size_sqm = models.PositiveIntegerField(default=28)
    total_rooms = models.PositiveIntegerField(default=10)
    amenities = models.TextField(help_text='Comma separated list, e.g. Free WiFi, Smart TV, Mini Bar')
    cover_image = models.ImageField(upload_to='rooms/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    floor_range = models.CharField(max_length=50, blank=True, default='2nd - 4th Floor')

    class Meta:
        ordering = ['base_price']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('rooms:detail', args=[self.slug])

    @property
    def amenities_list(self):
        return [a.strip() for a in self.amenities.split(',') if a.strip()]

    @property
    def rooms_available(self):
        return max(1, self.total_rooms - (self.id * 2 % self.total_rooms))


class RoomImage(models.Model):
    room_type = models.ForeignKey(RoomType, related_name='gallery', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='rooms/gallery/')
    caption = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return f"{self.room_type.name} image"
