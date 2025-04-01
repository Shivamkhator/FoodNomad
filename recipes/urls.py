from django.urls import path
from . import views

urlpatterns = [
    path('', views.display_recipes, name='home'),
    path('create_recipe/', views.create_recipe, name='create_recipe'),
    path('display_recipes/', views.display_recipes, name='display_recipes'),    
    path('recipe_detail/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('update_recipe/<int:recipe_id>/', views.update_recipe, name='update_recipe'),
    path('delete_recipe/<int:recipe_id>/', views.delete_recipe, name='delete_recipe'),    
]
