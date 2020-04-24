from rest_framework import serializers
from rest_polymorphic.serializers import PolymorphicSerializer
from .models import Item, Pizza, Drink


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class DrinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drink
        fields = '__all__'


class PizzaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pizza
        fields = '__all__'


class ItemPolymorphicSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        Item: ItemSerializer,
        Pizza: PizzaSerializer,
        Drink: DrinkSerializer
    }
