from __future__ import unicode_literals

from django.db import models

from django.utils.timezone import now

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit

from django.core.exceptions import ValidationError

from math import ceil

# Create your models here.

class IngredientCategory(models.Model):
    name = models.CharField(max_length=128)


    def __str__(self):
        return self.name

class Ingredient(models.Model):
    name = models.CharField(max_length=128, unique = True)
    amount = models.DecimalField(default=1, max_digits=5, decimal_places=2)
    store_choices = (('AH', 'Albert Heijn'), ('SL', 'Sligro'))
    store = models.CharField(max_length = 2, choices = store_choices, default = 'SL')
    category = models.ForeignKey(IngredientCategory, on_delete=models.CASCADE)
    description_of_amount = models.CharField(max_length=128, default = 'Per stuk')
    price = models.DecimalField(default=1, max_digits=5, decimal_places=2)

    def __str__(self):              # __unicode__ on Python 2
        return "%s | %s (%s)" % (self.category, self.name, self.description_of_amount)

    class Meta:
        ordering = ['category', 'name']
        verbose_name = 'Ingredient'
        verbose_name_plural = '1. Ingredienten'




def validate_mod_five(value):
    if value % 5 != 0:
        raise ValidationError( ('Only use time in steps of 5 (0, 5, 10, 15 etc.) - %(value)s does not fall in that category'), params={'value': value},  )

class RecipeCategory(models.Model):
    name = models.CharField(verbose_name="Category", max_length=128)

    def __str__(self):
        return self.name

class RecipeCame_From(models.Model):
    name = models.CharField(verbose_name="Origin", max_length=128)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    name = models.CharField(max_length=128)
    method=models.TextField(blank=True)
    dateadded = models.DateTimeField(default=now, blank=True)
    category = models.ForeignKey(RecipeCategory, on_delete=models.CASCADE)
    came_from = models.ForeignKey(RecipeCame_From, verbose_name="Came from", on_delete=models.CASCADE)
    ingredient = models.ManyToManyField(Ingredient, through='RecipeIngredient')
    time = models.IntegerField(default=15, validators=[validate_mod_five])
    image = models.ImageField(upload_to = 'recipes', blank=True)
    url = models.URLField(blank=True)

    image_thumbnail = ImageSpecField(source='image',
                                      processors=[ResizeToFit(100, 50)],
                                      format='JPEG',
                                      options={'quality': 90})

    image_large = ImageSpecField(source='image',
                                      processors=[ResizeToFit(1280, 720)],
                                      format='JPEG',
                                      options={'quality': 90})

    class Meta:
        verbose_name = 'Recept'
        verbose_name_plural = '2. Recepten'
        ordering = ['name']



    def _time_category(self):
        return str(int(10 * ceil(self.time / 10.0)))

    time_category = property(_time_category)

    def _get_price(self):
        price = 0
        t = RecipeIngredient.objects.select_related('ingredient').filter(recipe = self)

        for i in t:
            price += i.amount / i.ingredient.amount * i.ingredient.price
        return round(price,2)

    price = property(_get_price)



    def __str__(self):              # __unicode__ on Python 2
        return self.name

    def get_ingredients(self):
        t = RecipeIngredient.objects.filter(recipe = self)
        out = ''
        for i in t:
            out+=i.ingredient.name
            out+='\t'
            out+=str(i.amount)
            out+='\t'
            out+=str(i.ingredient.price)
            out+='\t'
            out+=str(i.ingredient.amount)
            out+='\n'
        return out #"\n".join([str(i.amount) for i in t])

    ingredients = property(get_ingredients)



class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.DecimalField(default=1, max_digits=5, decimal_places=2)

class Recipelist(models.Model):
    name = models.CharField(max_length=128)
    recipe = models.ManyToManyField(Recipe, through='RecipeRecipelist')
    dateadded = models.DateTimeField(default=now, blank=True)

    def __str__(self):
        return self.name

    def _recipes(self):
        out = ''
         #"\n".join([str(i.amount) for i in t])
        return ', '.join([str(i.recipe.name) for i in RecipeRecipelist.objects.select_related('recipe').filter(recipelist = self)])
        #for i in RecipeRecipelist.objects.filter(recipelist = self):
            #out+=i.recipe.name
        #return out

    recipes = property(_recipes)

    class Meta:
        verbose_name = 'Receptenlijst'
        verbose_name_plural = '3. Receptenlijsten'

class RecipeRecipelist(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    recipelist = models.ForeignKey(Recipelist, on_delete=models.CASCADE)

class Shoppinglist(models.Model):
    ingredient = models.ManyToManyField(Ingredient, through='ShoppinglistIngredient')
    name = models.CharField(max_length=128, default = 'Shoppinglist')
    dateadded = models.DateTimeField(default=now, blank=True)

    class Meta:
        verbose_name = 'Boodschappenlijst'
        verbose_name_plural = '4. Boodschappenlijsten'

class ShoppinglistIngredient(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    shoppinglist = models.ForeignKey(Shoppinglist, on_delete=models.CASCADE)
    amount = models.DecimalField(default=1, max_digits=5, decimal_places=2)
    def __str__(self):
        return '%s - %s' % (self.ingredient.name, self.amount)

    def _amount_to_buy(self):
        return int(ceil(self.amount))
    amount_to_buy = property (_amount_to_buy)
