from __future__ import unicode_literals

from django.db import models

from django.utils.timezone import now

# Create your models here.

class Ingredient(models.Model):
    name = models.CharField(max_length=128)
    amount = models.DecimalField(default=1, max_digits=5, decimal_places=2)
    store_choices = (('AH', 'Albert Heijn'), ('SL', 'Sligro'))
    store = models.CharField(max_length = 2, choices = store_choices, default = 'SL')
    description_of_amount = models.CharField(max_length=128)
    price = models.DecimalField(default=1, max_digits=5, decimal_places=2)

    def __str__(self):              # __unicode__ on Python 2
        return "%s (%s)" % (self.name, self.description_of_amount)




class Recipe(models.Model):
    name = models.CharField(max_length=128)
    method=models.TextField()
    ingredient = models.ManyToManyField(Ingredient, through='RecipeIngredient')
    time = models.IntegerField(default=15)

    def get_price(self):
        price = 0
        for i in self.ingredient.all():
            price += i__amount * i.price
        return price



    def __str__(self):              # __unicode__ on Python 2
        return self.name

    def get_ingredients(self):
        return "\n".join([i.name for i in self.ingredient.all()])

    get_ingredients.short_description = "Ingredients"

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.DecimalField(default=1, max_digits=5, decimal_places=2)

class Recipelist(models.Model):
    name = models.CharField(max_length=128)
    recipe = models.ManyToManyField(Recipe, through='RecipeRecipelist')

    def __str__(self):
        return self.name


class RecipeRecipelist(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    recipelist = models.ForeignKey(Recipelist, on_delete=models.CASCADE)

class Shoppinglist(models.Model):
    ingredient = models.ManyToManyField(Ingredient, through='ShoppinglistIngredient')
    name = models.CharField(max_length=128, default = 'Shoppinglist')
    dateadded = models.DateTimeField(default=now, blank=True)

class ShoppinglistIngredient(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    shoppinglist = models.ForeignKey(Shoppinglist, on_delete=models.CASCADE)
    amount = models.DecimalField(default=1, max_digits=5, decimal_places=2)
    def __str__(self):
        return '%s - %s' % (self.ingredient.name, self.amount)
