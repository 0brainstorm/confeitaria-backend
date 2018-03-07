# from django.conf.urls import url, include
# from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers
from recipes.views import UnitViewSet, IngredientViewSet, SubProductViewSet, IngredientPortionViewSet, ProductViewSet, SubProductPortionViewSet


router = routers.SimpleRouter()
router.register('units', UnitViewSet)
router.register('ingredients', IngredientViewSet)
router.register('subproducts', SubProductViewSet)
router.register('ingredient_portions', IngredientPortionViewSet)
router.register('products', ProductViewSet)
router.register('subproduct_portions', SubProductPortionViewSet)

urlpatterns = router.urls
