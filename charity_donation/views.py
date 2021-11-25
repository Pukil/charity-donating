from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views import View

from charity_donation.models import Donation, Institution, Category


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


class AddDonation(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request):
        context = {
            'categories': Category.objects.all(),
            'organisations': Institution.objects.all()
        }
        return render(request, 'charity_donation/form.html', context)

    def post(self, request):
        quantity = request.POST.get('bags')
        categories = request.POST.getlist('categories')
        institution = Institution.objects.get(pk=int(request.POST.get('organization')))
        address = request.POST.get('address')
        phone_number = int(request.POST.get('phone').replace(" ", ""))
        city = request.POST.get('city')
        zip_code = request.POST.get('postcode')
        pick_up_date = request.POST.get('data')
        pick_up_time = request.POST.get('time')
        pick_up_comment = request.POST.get('more_info')
        user = request.user
        instance = Donation.objects.create(quantity=quantity, institution=institution, address=address,
                                phone_number=phone_number, city=city, zip_code=zip_code, pick_up_date=pick_up_date,
                                pick_up_time=pick_up_time, pick_up_comment=pick_up_comment, user=user)
        for category in categories:
            instance.categories.add(category)
        return render(request, 'charity_donation/form-confirmation.html')


class ProfileView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'
    def get(self, request, pk):
        context = {'donations': Donation.objects.filter(user=User.objects.get(pk=pk))}
        return render(request, 'charity_donation/profile.html', context)


class Login(View):
    def get(self, request):
        return render(request, 'charity_donation/login.html')

    def post(self, request):
        username = request.POST.get('email')
        try:
            if User.objects.get(username=username):
                password = request.POST.get('password')
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect(reverse_lazy('landing-page'))
                else:
                    return redirect(reverse_lazy('login'))
        except User.DoesNotExist:
            return redirect(reverse_lazy('register'))


class LogOut(View):
    def get(self, request):
        logout(request)
        return redirect(reverse_lazy('landing-page'))


class Register(View):
    def get(self, request):
        return render(request, 'charity_donation/register.html')

    def post(self, request):
        login = request.POST.get('email')
        first_name = request.POST.get('name')
        last_name = request.POST.get('surname')
        if request.POST.get('password') == request.POST.get('password2'):
            password = request.POST.get('password')
            User.objects.create_user(login, password=password, first_name=first_name, last_name=last_name, email=login)
            return redirect(reverse_lazy('login'))
        else:
            return render(request, 'charity_donation/register.html', {'error_message': "Hasła nie są zgodne"})
