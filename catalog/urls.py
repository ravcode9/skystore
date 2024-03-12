from django.urls import path
from .views import index, home, contacts

urlpatterns = [
    path('', index, name='index'),
    path('home/', home, name='home'),
    path('contacts/', contacts, name='contacts'),
]