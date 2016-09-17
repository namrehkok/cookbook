from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

from .models import Recipelist, RecipeIngredient, Shoppinglist, ShoppinglistIngredient, Recipe, Ingredient, RecipeRecipelist

from django.db.models import F, FloatField, Sum
from math import ceil

def shoppinglist(request):
    SL = ShoppinglistIngredient.objects.filter(shoppinglist__name = 'Shopping List').order_by('ingredient__store', 'ingredient__category')
    output='<html><table>'
    Store = ''
    Cat = ''
    for i in SL:
        if i.ingredient.store <> Store:
            Store = i.ingredient.store
            output+='<tr><td><h1>%s</h1></td></tr>' % Store
        if i.ingredient.category.name <> Cat:
            Cat = i.ingredient.category.name
            output+='<tr><td><h2>%s</h2></td></tr>' % Cat
        output+='<tr><td>%s</td><td>%s</td></tr>' % (str(i.ingredient.name), i.amount_to_buy)
    output+='</table></html>'
    return HttpResponse(output)

def tst(request):
    recept = Recipe.objects.get(name = 'd')
    ingredient = Ingredient.objects.get(name = '1')
    t = RecipeIngredient.objects.filter(recipe = recept, ingredient = ingredient).values('ingredient').annotate(score = Sum('amount'))
    output = str(t.get(ingredient = ingredient)['score'])
    for i in t:
        output += str(i)

    return HttpResponse(output)

'''
    output = ''
    #sl = Shoppinglist.objects.get(name = 'New list2')
    s = ShoppinglistIngredient.objects.filter(shoppinglist__name = 'MyShoppingList').values(
        'ingredient__name').annotate(score = Sum('amount'))
    for ingredient in s:
        output += ingredient['ingredient__name']
        output += str(ceil(ingredient['score']))
        output += str('<br>')
    return HttpResponse(output)

def index(request):
    r = Recipe.objects.get(name = 'Andere curry')
    for i in r:
        output += str(i)

    return output
'''
