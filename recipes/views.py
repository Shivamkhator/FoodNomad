from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Recipe, Ingredient

def home(request):
    return HttpResponse("Recipes Page!")

@login_required
def create_recipe(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        instructions = request.POST.get('instructions')
        vegetarian = request.POST.get('vegetarian') == 'on'
        ingredients_list = request.POST.getlist('ingredients')  # User-submitted ingredients

        recipe = Recipe.objects.create(
            title=title, description=description, instructions=instructions, 
            author=request.user, vegetarian=vegetarian
        )

        # Adding ingredients (without nutritional info)
        for ingredient in ingredients_list:
            Ingredient.objects.create(recipe=recipe, name=ingredient, quantity="1 unit")  # Default quantity

        messages.success(request, "Recipe created successfully!")
        return redirect('display_recipes')
    
    return render(request, 'create_recipe.html')

def display_recipes(request):
    recipes = Recipe.objects.all()
    return render(request, 'display_recipes.html', {'recipes': recipes})

def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    ingredients = recipe.ingredients.all()
    return render(request, 'recipe_detail.html', {'recipe': recipe, 'ingredients': ingredients})

@login_required
def update_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)

    # Ensure only the author or an admin can edit
    if request.user != recipe.author and not request.user.is_superuser:
        messages.error(request, "You are not authorized to update this recipe.")
        return redirect('recipe_detail', recipe_id=recipe.id)

    if request.method == "POST":
        recipe.title = request.POST.get('title')
        recipe.description = request.POST.get('description')
        recipe.instructions = request.POST.get('instructions')
        recipe.vegetarian = request.POST.get('vegetarian') == 'on'
        recipe.save()
        messages.success(request, "Recipe updated successfully!")
        return redirect('recipe_detail', recipe_id=recipe.id)

    return render(request, 'update_recipe.html', {'recipe': recipe})

@login_required
def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)

    # Allow only the author or an admin to delete
    if request.user != recipe.author and not request.user.is_superuser:
        messages.error(request, "You are not authorized to delete this recipe.")
        return redirect('recipe_detail', recipe_id=recipe.id)

    recipe.delete()
    messages.success(request, "Recipe deleted successfully!")
    return redirect('display_recipes')
