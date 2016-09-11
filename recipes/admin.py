from django.contrib import admin
from imagekit.admin import AdminThumbnail
from django.conf.urls import url

from django import forms
# Register your models here.

from .models import Recipe, Ingredient, RecipeIngredient, Recipelist, RecipeRecipelist, Shoppinglist, ShoppinglistIngredient, IngredientCategory, RecipeCategory, RecipeCame_From

from django.db.models import Sum

import os.path


#admin.site.register(Recipe)
#admin.site.register(Ingredient)
#admin.site.register(RecipeIngredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'amount', 'store', 'description_of_amount', 'price' )
    list_filter = ('store', 'category__name')

admin.site.register(Ingredient, IngredientAdmin)


class IngredientInline(admin.TabularInline):
    #model=Recipe#.ingredient.through

    model = RecipeIngredient
    extra = 1

def add_name_to_button(button_nm = 'Edit...'):
    """
    An edit button, ah... it looks so nice (it does!).
    """

    def edit_button(self, obj):
        on_click = "window.location='%d';" % obj.id
        return '<input type="button" onclick="%s" value="%s" />' % (on_click, button_nm)
    return edit_button



class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'time', 'get_category', 'get_came_from', 'price',)

    edit_button = add_name_to_button('Edit')
    edit_button.allow_tags = True
    edit_button.short_description = 'edit'

    def link_image(self, obj):
        if os.path.isfile(obj.image.path):
            output = '<a href = "%s"><img src = "%s"</a>' % (obj.image_large.url, obj.image_thumbnail.url)
        else:
            output = 'Geen foto'
        return output


    link_image.allow_tags = True
    link_image.short_description = ''

    def get_category(self, obj):
        return obj.category.name
    get_category.short_description = 'Category'

    def get_came_from(self, obj):
        return obj.came_from.name
    get_came_from.short_description = 'Came from'

    image_display = AdminThumbnail(image_field = 'image_thumbnail')
    image_display.short_description = ''

    def method__custom_rendering(self, obj):
        return "<pre>%s</pre>" % (obj.method,)
    method__custom_rendering.allow_tags = True
    method__custom_rendering.short_description = 'Method'

    readonly_fields = ('dateadded', )

    search_fields = ['name']
    list_filter = ('time', 'category__name', 'came_from__name')
    inlines = (IngredientInline,)
    actions = ['populate_recipelist', 'start_new_week', ]
    def populate_recipelist(modeladmin, request, queryset):
        s, created = Recipelist.objects.get_or_create(name = 'Recipe List')
        #s.save()
        for recept in queryset.all():
            t = RecipeRecipelist.objects.create(recipe = recept, recipelist = s)
    populate_recipelist.short_description = "Add items to recipe list"

    def start_new_week(modeladmin, request, queryset):
        '''
        add the recipes that are on the current list to the historical list and delete the recipes and ingredients from the shopping list
        '''

        rl = 'Recipe List'
        sl1 = 'Shopping List'
        sl2 = 'All ingredients (not aggregated)'

        rlo = Recipelist.objects.get(name = rl)
        s, created = Recipelist.objects.get_or_create(name = 'Recipe lists history')

        for i in RecipeRecipelist.objects.select_related('recipe').filter(recipelist = rlo):
            t = RecipeRecipelist.objects.create(recipe = i.recipe, recipelist = s)

        Recipelist.objects.filter(name = rl).delete()
        Shoppinglist.objects.filter(name = sl1).delete()
        Shoppinglist.objects.filter(name = sl2).delete()
    start_new_week.short_description = "Start a new week and clear all recipes and shopping lists"






admin.site.register(Recipe, RecipeAdmin)

# The recipelist



class RecipeInline(admin.TabularInline):
    #fieldsets = ('name',)
    model = RecipeRecipelist
    extra = 1

class RecipelistAdmin(admin.ModelAdmin):
    list_display = ('name', 'dateadded', 'recipes', )
    readonly_fields = ('name', 'dateadded', )
    inlines = (RecipeInline,)
    actions = ['populate_ingredient_shopping_list']
    def populate_ingredient_shopping_list(modeladmin, request, queryset):
        #Shoppinglist.objects.filter(name = 'MyTempList').delete()
        s, created = Shoppinglist.objects.get_or_create(name = 'All ingredients (not aggregated)')
        #s.save()
        for lijst in queryset.all():
            for recept in lijst.recipe.all():
                for ingredient in recept.ingredient.all():
                    t = RecipeIngredient.objects.get(recipe = recept, ingredient = ingredient)
                    si = ShoppinglistIngredient.objects.create(ingredient = ingredient, shoppinglist = s, amount = t.amount / ingredient.amount)

        Shoppinglist.objects.filter(name = 'Shopping List').delete()

        SL = ShoppinglistIngredient.objects.filter(shoppinglist__name = 'All ingredients (not aggregated)').values('ingredient').annotate(score = Sum('amount'))

        s, created = Shoppinglist.objects.get_or_create(name = 'Shopping List')

        for i in SL:
            ShoppinglistIngredient.objects.create(ingredient = Ingredient.objects.get(id=i['ingredient']), shoppinglist = s, amount = i['score'])

    populate_ingredient_shopping_list.short_description = "Create shopping list for selected items"


admin.site.register(Recipelist, RecipelistAdmin)

class IngredientInline2(admin.TabularInline):
    list_display = ('amount', 'amount_to_buy')
    model = ShoppinglistIngredient
    extra = 1

class ShoppinglistAdmin(admin.ModelAdmin):
    list_display = ('name', 'dateadded')
    inlines = (IngredientInline2,)
    readonly_fields = ('name', 'dateadded')

admin.site.register(Shoppinglist, ShoppinglistAdmin)
admin.site.register(IngredientCategory)
admin.site.register(RecipeCategory)
admin.site.register(RecipeCame_From)
