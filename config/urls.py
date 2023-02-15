from django.contrib import admin
from django.urls import path
from .api_router import api
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', api.urls)
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
