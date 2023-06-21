from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('users/',include('users.urls')),
    path('company/',include('Company.urls')),
    path('internships/',include('Internships.urls')),
    path('placements/',include('Placements.urls')),
    path('news/',include('News.urls')),
    path('admin/', admin.site.urls),
]
