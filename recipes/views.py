from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

from .models import Recipelist, RecipeIngredient, Shoppinglist, ShoppinglistIngredient, Recipe

from django.db.models import F, FloatField, Sum
from math import ceil

def shoppinglist(request):
    output = ''
    #sl = Shoppinglist.objects.get(name = 'New list2')
    s = ShoppinglistIngredient.objects.filter(shoppinglist__name = 'Shoppinglist').values(
        'ingredient__name').annotate(score = Sum('amount'))
    for ingredient in s:
        output += ingredient['ingredient__name']
        output += str(ceil(ingredient['score']))
        output += str('<br>')
    return HttpResponse(output)
'''
def index(request):
    r = Recipe.objects.get(name = 'Andere curry')
    for i in r:
        output += str(i)

    return output
'''
