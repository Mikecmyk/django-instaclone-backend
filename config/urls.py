# config/urls.py

from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from django.conf import settings 
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Authentication URLs
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'), 
    
    # Users and Profile Endpoints
    path('api/', include('users.urls')),
    
    # Post Endpoints (NEW)
    path('api/', include('content.urls')), # <-- Add the new content URLs
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)