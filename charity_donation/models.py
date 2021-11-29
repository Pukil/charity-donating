from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Category(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=128, null=True, default="Brak kategorii")


class Institution(models.Model):
    def __str__(self):
        return self.name

    CHOICES = (
        ('fundacja', 'fundacja'),
        ('organizacja pozarządowa', 'organizacja pozarządowa'),
        ('zbiórka lokalna', 'zbiórka lokalna'),
    )
    name = models.CharField(max_length=128)
    description = models.TextField()
    categories = models.ManyToManyField(Category)
    type = models.CharField(max_length=128, choices=CHOICES, default=CHOICES[0])

    def get_cat(self):
        return_string = ""
        for cat in self.categories.all():
            return_string += f"{cat.name}, "

        return return_string.rstrip(", ")

class Donation(models.Model):
    quantity = models.IntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.TextField()
    phone_number = models.IntegerField()
    city = models.CharField(max_length=64)
    zip_code = models.CharField(max_length=6)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None, blank=True)
    is_taken = models.BooleanField(default=False, blank=True, null=True)
    taken_check_date = models.DateField(default=None, blank=True, null=True)

    def get_cat(self):
        return_string = ""
        for cat in self.categories.all():
            return_string += f"{cat.name}, "

        return return_string.rstrip(", ")

    def __str__(self):
        return f"Organizacja: {self.institution}, Kategorie: {self.get_cat()}, ilość worków: {self.quantity}"
