from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/users/', include('apps.users.urls')),
    path('api/auth/', include('apps.users_auth.urls')),
    path('api/cars/', include('apps.cars.urls')),
    path('api/listings/', include('apps.listings.urls')),
    path('api/currencies/', include('apps.currency.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)