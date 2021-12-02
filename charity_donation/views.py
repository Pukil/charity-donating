import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View

from charity_donation.models import Donation, Institution, Category
from charity_donation.tokens import account_activation_token


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
        context = {
            'donations_taken': Donation.objects.filter(user=User.objects.get(pk=pk)).filter(is_taken=True).order_by('pick_up_date'),
            'donations_waiting': Donation.objects.filter(user=User.objects.get(pk=pk)).filter(is_taken=False).order_by('-pick_up_date')
        }
        return render(request, 'charity_donation/profile.html', context)

    def post(self, request, pk):
        donations = Donation.objects.filter(user=request.user)
        for donation in donations:
            if request.POST.get(f"is_taken_{donation.pk}"):
                donation.is_taken = True
                donation.taken_check_date = datetime.date.today()
                donation.save()
            else:
                donation.is_taken = False
                donation.save()
        return redirect(reverse_lazy(f'profile', kwargs={'pk': pk}))


class EditProfileView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request, pk):
        return render(request, 'charity_donation/edit_profile.html')

    def post(self, request, pk):
        user_instance = request.user
        if 'change_password' in request.POST:
            if user_instance.check_password(request.POST.get('old_pass')):
                new_password = request.POST.get('new_pass_1')
                new_password_confirm = request.POST.get('new_pass_2')
                if new_password == new_password_confirm:
                    user_instance.set_password(new_password)
                    user_instance.save()
                    user = authenticate(request, username=user_instance.username, password=new_password)
                    login(request, user)
                    return render(request, 'charity_donation/edit_profile.html', {'error_message': 'Zmieniono hasło'})
                else:
                    return render(request, 'charity_donation/edit_profile.html', {'error_message': 'Wprowadzone hasła różnią się'})
            else:
                return render(request, 'charity_donation/edit_profile.html', {'error_message': 'Wprowadzono niepoprawne hasło!'})
        else:
            if user_instance.check_password(request.POST.get('password')):
                user_instance.first_name = request.POST.get('first_name')
                user_instance.last_name = request.POST.get('last_name')
                user_instance.email = request.POST.get('email')
                user_instance.username = user_instance.email
                user_instance.save()
                return render(request, 'charity_donation/edit_profile.html', {'error_message': 'Zmieniono dane'})
            else:
                return render(request, 'charity_donation/edit_profile.html', {'error_message': 'Wprowadzono niepoprawne hasło!'})


class Login(View):
    def get(self, request):
        if 'success_activation' in request.session:
            context = {'error_message': request.session['success_activation']}
            del request.session['success_activation']
            return render(request, 'charity_donation/login.html', context)
        else:
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
                elif not user.is_active:
                    return render(request, 'charity_donation/login.html', {'error_message': "Proszę aktywować konto"})
                else:
                    return render(request, 'charity_donation/login.html', {'error_message': "Błędne hasło"})
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
            user = User.objects.create_user(login, password=password, first_name=first_name, last_name=last_name, email=login)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Aktywuj swoje konto'
            message = render_to_string('charity_donation/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = login
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return render(request, 'charity_donation/email_sent.html')
        else:
            return render(request, 'charity_donation/register.html', {'error_message': "Hasła nie są zgodne"})

class ActivateAccount(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            request.session['success_activation'] = 'Twój adres e-mail został potwierdzony. Możesz się teraz zalogować'
            return redirect(reverse_lazy('login'))

        return render(request, 'charity_donation/activation_failed.html', {'user': user})
