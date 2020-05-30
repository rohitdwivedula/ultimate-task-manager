from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls')),
    path('api/main/', include('tasks.api_urls')),
    path('', include('tasks.html_urls')),
 ]