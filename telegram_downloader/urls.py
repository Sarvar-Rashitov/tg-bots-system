from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', core_views.dashboard, name='dashboard'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('bots/', include('bots.urls')),
    path('users/', include('users.urls')),
    path('downloads/', include('downloads.urls')),
    path('broadcasts/', include('broadcasts.urls')),
    path('subscriptions/', include('subscriptions.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
