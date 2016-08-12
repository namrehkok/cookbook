from django.contrib import admin

# Register your models here.

from .models import Recipe, Ingredient, RecipeIngredient, Recipelist, RecipeRecipelist, Shoppinglist, ShoppinglistIngredient

#admin.site.register(Recipe)
#admin.site.register(Ingredient)
#admin.site.register(RecipeIngredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'store', 'description_of_amount' )

admin.site.register(Ingredient, IngredientAdmin)

class IngredientInline(admin.TabularInline):
    #model=Recipe#.ingredient.through
    model = RecipeIngredient
    extra = 1

class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'method', 'time' )
    inlines = (IngredientInline,)

admin.site.register(Recipe, RecipeAdmin)

# The recipelist



class RecipeInline(admin.TabularInline):
    model = RecipeRecipelist
    extra = 1

class RecipelistAdmin(admin.ModelAdmin):
    list_display = ('name', )
    inlines = (RecipeInline,)
    actions = ['populate_ingredient_shopping_list']
    def populate_ingredient_shopping_list(modeladmin, request, queryset):
        s = Shoppinglist()
        s.save()
        for lijst in queryset.all():
            for recept in lijst.recipe.all():
                for ingredient in recept.ingredient.all():
                    t = RecipeIngredient.objects.get(recipe = recept, ingredient = ingredient)
                    #output += str(ingredient.name)
                    #output += str(ingredient.amount)
                    #output += str(t.amount)
                    #output += str('<br>')
                    si = ShoppinglistIngredient.objects.create(ingredient = ingredient, shoppinglist = s, amount = t.amount / ingredient.amount)



    populate_ingredient_shopping_list.short_description = "Create shopping list for selected items"


admin.site.register(Recipelist, RecipelistAdmin)

class IngredientInline2(admin.TabularInline):
    #list_display = ('ingredient.name', 'ingredient.amount', 'description_of_amount')
    model = ShoppinglistIngredient
    extra = 1

class ShoppinglistAdmin(admin.ModelAdmin):
    list_display = ('name', 'dateadded')
    inlines = (IngredientInline2,)

admin.site.register(Shoppinglist, ShoppinglistAdmin)
