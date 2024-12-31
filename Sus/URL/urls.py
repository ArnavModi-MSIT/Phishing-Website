# filepath: /c:/Coding/Phishing-Website/Sus/URL/urls.py
from django.urls import path
from . import views  # Import views from the current package

urlpatterns = [
    path('', views.check_url, name='check_url'),  # Maps the root URL to the check_url view
]
