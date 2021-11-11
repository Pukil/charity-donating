from django.shortcuts import render

# Create your views here.
from django.views import View

from charity_donation.models import Donation, Institution


class LandingPage(View):
    def get(self, request):
        bags = 0
        institutions = 0
        for donation in Donation.objects.all():
            bags += donation.quantity

        for _ in Institution.objects.all():
            institutions += 1

        context = {
            'bags_count': bags,
            'institution_count': institutions,
            'foundations': Institution.objects.filter(type='fundacja'),
            'organisations': Institution.objects.filter(type='organizacja pozarządowa'),
            'locals': Institution.objects.filter(type='zbiórka lokalna')
        }
        return render(request, 'charity_donation/index.html', context)


class AddDonation(View):
    def get(self, request):
        return render(request, 'charity_donation/form.html')


class Login(View):
    def get(self, request):
        return render(request, 'charity_donation/login.html')


class Register(View):
    def get(self, request):
        return render(request, 'charity_donation/register.html')
