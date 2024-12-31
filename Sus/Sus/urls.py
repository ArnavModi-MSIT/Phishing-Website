from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('URL.urls')),  # Include URL app's URLs at the root
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
