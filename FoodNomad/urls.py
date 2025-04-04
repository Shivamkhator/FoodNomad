
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('recommendations/', include('recommendations.urls')),
    path('recipes/', include('recipes.urls')),
    path('accounts/', include('allauth.urls')),
    path('',include('recommendations.urls')),
]