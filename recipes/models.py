from django.db import models

SOLID_UNITS = (('mg', 'miligrama'), ('g', 'grama'), ('kg', 'kilograma'))
LIQUID_UNITS = (('ml', 'mililitro'), ('l', 'litro'), ('us_cup', 'xícara'),
                ('us_tbsp', 'colher de sopa'), ('us_tsp', 'colher de chá'))


class Unit(models.Model):
    value = models.CharField(unique=True, max_length=8)
    text = models.CharField(max_length=30)


class Ingredient(models.Model):
    name = models.CharField(unique=True, max_length=30)
    price = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    unit = models.ForeignKey(to=Unit, on_delete=models.PROTECT, related_name='ingredients')
    amount = models.DecimalField(default=0, max_digits=5, decimal_places=2)

    def __unicode__(self):
        return self.name


class IngredientPortion(models.Model):
    ingredient = models.ForeignKey('Ingredient', on_delete=models.PROTECT)
    amount = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    subproduct = models.ForeignKey('SubProduct',
        on_delete=models.CASCADE,
        related_name='portions')


class SubProduct(models.Model):
    name = models.CharField(unique=True, max_length=30)


class SubProductPortion(models.Model):
    subproduct = models.ForeignKey('SubProduct', on_delete=models.PROTECT)
    amount = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    unit = models.ForeignKey(to=Unit, on_delete=models.PROTECT, related_name='subproduct_portions')
    product = models.ForeignKey('Product',
        on_delete=models.PROTECT,
        related_name='portions')


class Product(models.Model):
    name = models.CharField(unique=True, max_length=30)
