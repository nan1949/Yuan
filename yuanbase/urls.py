from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/vocal/', include('vocal.urls')),
    path('api/users/', include('users.urls')),
    path('auth/', obtain_auth_token)
]


urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)