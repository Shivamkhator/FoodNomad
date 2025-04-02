from django.contrib import admin
from .models import Recipe, Ingredient, IngredientQuantity

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'vegetarian')
    search_fields = ('title', 'author__username')
    list_filter = ('vegetarian', 'created_at')
    ordering = ('-created_at',)

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'calories', 'proteins', 'carbohydrates', 'fats', 'sugar')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(IngredientQuantity)
class IngredientQuantityAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'quantity')
    search_fields = ('recipe__title', 'ingredient__name')
