from rest_framework import routers
from .views import CategoryViewSet, InstitutionViewSet
from django.urls import include, path

router = routers.DefaultRouter()
router.register(r'category', CategoryViewSet)
router.register(r'institution', InstitutionViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
