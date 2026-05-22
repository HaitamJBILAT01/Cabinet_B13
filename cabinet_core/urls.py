"""
URL configuration for Cabinet B13.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from comptes.views import CustomLoginView
from dossiers.views import dashboard

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Dashboard (root)
    path('', dashboard, name='dashboard'),

    # Authentication
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),

    # Dossiers app
    path('', include('dossiers.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)