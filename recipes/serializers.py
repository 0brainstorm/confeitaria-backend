from decimal import Decimal, ROUND_05UP

from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField, SerializerMethodField
from recipes.models import Unit, Ingredient, SubProduct, IngredientPortion, Product, SubProductPortion


class UnitSerializer(ModelSerializer):
    class Meta:
        model = Unit
        fields = ('id', 'value', 'text')

        extra_kwargs = {
            'value': {
                    'validators': [],
            }
        }


class IngredientSerializer(ModelSerializer):
    info = SerializerMethodField()

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'price', 'amount', 'unit', 'info')
        read_only_fields = ('unit',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['unit'] = UnitSerializer(context=self.context)

    def create(self, validated_data):
        unit_data = validated_data.pop('unit')
        unit = Unit.objects.get(**unit_data)
        instance = Ingredient.objects.create(unit=unit, **validated_data)
        return instance

    def update(self, i, validated_data):
        unit_data = validated_data.pop('unit')
        unit = Unit.objects.get(**unit_data)
        i.name = validated_data.get('name', i.name)
        i.price = validated_data.get('price', i.price)
        i.amount = validated_data.get('amount', i.amount)
        i.unit = unit
        i.save()
        return i

    def get_info(self, i):
        text = '{} {} por R$ {}'.format(i.amount, i.unit.text, i.price)
        return text


class SubProductSerializer(ModelSerializer):
    total = SerializerMethodField()

    class Meta:
        model = SubProduct
        fields = ('id', 'name', 'portions', 'total')
        read_only_fields = ('portions',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['portions'] = IngredientPortionSerializer(
            many=True, context=self.context, read_only=True)

    def get_total(self, sp):
        total = 0
        for p in sp.portions.all():
            i = p.ingredient
            total += p.amount * (i.price/i.amount)
        return Decimal(total).quantize(Decimal('.01'), rounding=ROUND_05UP)


class IngredientPortionSerializer(ModelSerializer):
    ingredient = PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    subproduct = PrimaryKeyRelatedField(queryset=SubProduct.objects.all())
    info = SerializerMethodField()

    class Meta:
        model = IngredientPortion
        fields = ('id', 'ingredient', 'subproduct', 'amount', 'info')

    def get_info(self, ip):
        price = ip.amount * (ip.ingredient.price/ip.ingredient.amount)
        total = 0
        for spp in ip.subproduct.portions.all():
            i = spp.ingredient
            total += spp.amount * (i.price / i.amount)
        share = price / total
        return '{:.2f} {} por R$ {:.2f} ({:.2%})'.format(ip.amount, ip.ingredient.unit.text, price, share)


class ProductSerializer(ModelSerializer):
    total = SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'portions', 'total')
        read_only_fields = ('portions',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['portions'] = SubProductPortionSerializer(
            many=True, read_only=True, context=self.context)

    def get_total(self, p):
        total = 0
        for spp in p.portions.all():
            sp_cost = 0
            for ip in spp.subproduct.portions.all():
                sp_cost += ip.amount * (ip.ingredient.price/ip.ingredient.amount)
            total += spp.amount * sp_cost
        return Decimal(total).quantize(Decimal('.01'), rounding=ROUND_05UP)


class SubProductPortionSerializer(ModelSerializer):
    subproduct = PrimaryKeyRelatedField(queryset=SubProduct.objects.all())
    product = PrimaryKeyRelatedField(queryset=Product.objects.all())
    unit = PrimaryKeyRelatedField(queryset=Unit.objects.all())

    class Meta:
        model = SubProductPortion
        fields = ('id', 'subproduct', 'product', 'amount', 'unit')
