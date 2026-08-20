from django.db import models


class MenuCategory(models.Model):
    name = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Menu categories'

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    category = models.ForeignKey(MenuCategory, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=255, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_signature = models.BooleanField(default=False)
    is_available_room_service = models.BooleanField(default=True)
    spice_level = models.PositiveSmallIntegerField(default=0, help_text='0-3 chili icons')

    class Meta:
        ordering = ['category__order', 'name']

    def __str__(self):
        return self.name
