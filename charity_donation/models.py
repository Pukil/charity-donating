from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=128, null=True, default="Brak kategorii")


class Institution(models.Model):
    CHOICES = (
        ('fundacja', 'fundacja'),
        ('organizacja pozarządowa', 'organizacja pozarządowa'),
        ('zbiórka lokalna', 'zbiórka lokalna'),
    )
    name = models.CharField(max_length=128)
    description = models.TextField()
    categories = models.ManyToManyField(Category)
    type = models.CharField(max_length=128, choices=CHOICES, default=CHOICES[0])
