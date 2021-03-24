from rest_framework import serializers
from .models import Recipe, Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['name']


class RecipeSerializer(serializers.ModelSerializer):
    """ A `Recipe` is a list of ingredients. """
    ingredients = IngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'description', 'ingredients']

    def create(self, validated_data) -> Recipe:
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        for ingredient_data in ingredients_data:
            Ingredient.objects.create(recipe=recipe, **ingredient_data)
        return recipe

    def update(self, instance, validated_data) -> Recipe:
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.filter(id=instance.id).update(**validated_data)
        Ingredient.objects.filter(recipe=recipe).delete()
        for ingredient_data in ingredients_data:
            Ingredient.objects.create(recipe=recipe, **ingredient_data)
        return recipe
