from django.contrib import admin

# Register your models here.
from charity_donation.models import Category, Institution, Donation

admin.site.register(Category)
admin.site.register(Institution)
admin.site.register(Donation)