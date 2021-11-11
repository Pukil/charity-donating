from django.shortcuts import render

# Create your views here.
from django.views import View


class LandingPage(View):
    def get(self, request):
        return render(request, 'charity_donation/index.html')