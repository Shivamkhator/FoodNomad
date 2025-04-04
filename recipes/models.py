from django.db import models
from django.contrib.auth.models import User


from django.utils import timezone

class Recipe(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    instructions = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    vegetarian = models.BooleanField(default=False)
    image = models.ImageField(upload_to='recipe_images/', null=True, blank=True)

    created_at = models.DateTimeField(default=timezone.now)  # 👈 Add this


    def __str__(self):
        return self.title


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    fats = models.FloatField(default=0.0)  # Default value
    carbohydrates = models.FloatField(default=0.0)  # Default value
    proteins = models.FloatField(default=0.0)  # Default value
    calories = models.FloatField(default=0.0)  # Default value
    sugar = models.FloatField(default=0.0)  # Default value

    def __str__(self):
        return self.name


    def __str__(self):
        return self.name


class IngredientQuantity(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='ingredients', on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)  # Corrected field name
    quantity = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.quantity} of {self.ingredient.name} for {self.recipe.title}"
