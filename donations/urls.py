"""donations URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from charity_donation.views import LandingPage, Login, Register, AddDonation, LogOut, ProfileView, EditProfileView, \
    ActivateAccount, PasswordReset

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPage.as_view(), name='landing-page'),
    path('login/', Login.as_view(), name='login'),
    path('register/', Register.as_view(), name='register'),
    path('add_donation/', AddDonation.as_view(), name='add-donation'),
    path('logout/', LogOut.as_view(), name='logout'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('profile/edit/<int:pk>/', EditProfileView.as_view(), name='edit-profile'),
    path('activate_user/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate-acc'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='charity_donation/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="charity_donation/password_reset_confirm.html"),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='charity_donation/password_reset_complete.html'),
         name='password_reset_complete'),
    path('password_reset/', PasswordReset.as_view(), name='password-reset' )
]
