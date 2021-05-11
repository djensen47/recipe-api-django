from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Recipe, Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['name']


class RecipeSerializer(serializers.ModelSerializer):
    """
    A `Recipe` is a list of ingredients with a name and description.
    """
    ingredients = IngredientSerializer(many=True, allow_null=True, required=False)

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'description', 'ingredients']

    def create(self, validated_data) -> Recipe:
        ingredients_data = validated_data.pop('ingredients', [])
        recipe = Recipe.objects.create(**validated_data)
        for ingredient_data in ingredients_data:
            Ingredient.objects.create(recipe=recipe, **ingredient_data)
        return recipe

    def update(self, instance, validated_data) -> Recipe:
        ingredients_data = validated_data.pop('ingredients', [])
        recipe = super().update(instance, validated_data)
        Ingredient.objects.filter(recipe=recipe).delete()
        for ingredient_data in ingredients_data:
            Ingredient.objects.create(recipe=recipe, **ingredient_data)
        return recipe

    def validate(self, data):
        super().validate(data)
        if hasattr(self, 'initial_data'):
            unknown_keys = set(self.initial_data.keys()) - set(self.fields.keys())
            if unknown_keys:
                raise ValidationError("Unknown fields: {}".format(unknown_keys))
        return data
