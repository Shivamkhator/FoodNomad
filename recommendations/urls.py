from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('stores/',views.stores, name='stores'),
    path('grocery_stores/', views.grocery_stores_view, name='grocery_stores'),
    path('filtered_recipes/', views.filtered_recipes, name='filtered_recipes'),
    
]
