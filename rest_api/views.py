from django.shortcuts import render
from charity_donation.models import Institution, Category
from rest_framework import viewsets
from .serializers import InstitutionSerializer, CategorySerializer
# Create your views here.

class InstitutionViewSet(viewsets.ModelViewSet):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

