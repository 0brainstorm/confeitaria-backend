from django.shortcuts import render
# from django.http import HttpResponse

from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
# from rest_framework.decorators import list_route

from recipes.models import Unit, Ingredient, IngredientPortion, SubProduct, SubProductPortion, Product
from recipes.serializers import UnitSerializer, IngredientSerializer, IngredientPortionSerializer, SubProductSerializer, SubProductPortionSerializer, ProductSerializer


def index(request):
    return render(request, 'index.html')


class UnitViewSet(ReadOnlyModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer


class IngredientViewSet(ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class IngredientPortionViewSet(ModelViewSet):
    queryset = IngredientPortion.objects.all()
    serializer_class = IngredientPortionSerializer


class SubProductViewSet(ModelViewSet):
    queryset = SubProduct.objects.all()
    serializer_class = SubProductSerializer


class SubProductPortionViewSet(ModelViewSet):
    queryset = SubProductPortion.objects.all()
    serializer_class = SubProductPortionSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
