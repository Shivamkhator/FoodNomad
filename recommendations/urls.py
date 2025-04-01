from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('shops/', views.grocery_stores_view, name='grocery_stores')
    
]
