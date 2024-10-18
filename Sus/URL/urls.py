from django.urls import path
from . import views  # Import views from the current package

urlpatterns = [
    path('', views.index, name='index'),  # Maps the root URL to the index view
    path('check-url/', views.check_url, name='check_url'),  # Maps the 'check-url/' path to the check_url view
]
