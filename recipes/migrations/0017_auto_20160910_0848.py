# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-10 08:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0016_recipelist_dateadded'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredient',
            options={'ordering': ['category', 'name'], 'verbose_name': 'Ingredient', 'verbose_name_plural': '1. Ingredienten'},
        ),
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ['name'], 'verbose_name': 'Recept', 'verbose_name_plural': '2. Recepten'},
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=6),
        ),
    ]
