from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Recipe, Ingredient, IngredientQuantity

def home(request):
    return HttpResponse("Recipes Page!")

@login_required
def create_recipe(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        instructions = request.POST.get('instructions')
        vegetarian = request.POST.get('vegetarian') == 'on'
        image = request.FILES.get('image')

        recipe = Recipe.objects.create(
            title=title, description=description, instructions=instructions,
            author=request.user, vegetarian=vegetarian, image=image
        )

        ingredient_names = request.POST.getlist('ingredient_name')
        ingredient_quantities = request.POST.getlist('ingredient_quantity')

        for name, quantity in zip(ingredient_names, ingredient_quantities):
            ingredient, _ = Ingredient.objects.get_or_create(name=name)
            IngredientQuantity.objects.create(
                recipe=recipe, ingredient=ingredient, quantity=quantity
            )

        messages.success(request, "Recipe created successfully!")
        return redirect('display_recipes')

    return render(request, 'create_recipe.html')

def display_recipes(request):
    recipes = Recipe.objects.all().order_by('-created_at')  # shows latest first
    return render(request, 'display_recipes.html', {'recipes': recipes})

def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    ingredients = IngredientQuantity.objects.filter(recipe=recipe)
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
