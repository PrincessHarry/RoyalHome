from django.db import models
from django.urls import reverse


class BlogPost(models.Model):
    CATEGORY_CHOICES = [
        ('travel', 'Travel Tips'),
        ('local', 'Local Attractions'),
        ('hotel-news', 'Hotel News'),
        ('food', 'Food & Dining'),
    ]
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='travel')
    excerpt = models.CharField(max_length=300)
    content = models.TextField()
    cover_image = models.ImageField(upload_to='blog/', blank=True, null=True)
    author = models.CharField(max_length=100, default='Xceptional Place Team')
    published_date = models.DateField()

    class Meta:
        ordering = ['-published_date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', args=[self.slug])
