

from django.urls import path, include
from .views import checkurl

urlpatterns = [
    path('', checkurl, name='checkurl'),
]
