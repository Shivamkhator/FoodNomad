from django.contrib import admin
from .models import Recipe, Ingredient

class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'recipe')
    readonly_fields = ('recipe', 'name', 'quantity')  # Users cannot edit these
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser  # Only admin can change

admin.site.register(Recipe)
admin.site.register(Ingredient, IngredientAdmin)
