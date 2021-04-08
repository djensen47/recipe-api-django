from django.test import TestCase
from assertpy import assert_that
from rest_framework import status
from rest_framework.test import APIClient
from .factories import RecipeFactory, IngredientFactory
from ..models import Recipe, Ingredient
import factory

LIST_SIZE = 3


class RecipeCreateTestCase(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_should_return_404(self) -> None:
        response = self.client.delete(f'/recipes/1000')
        assert_that(response.status_code).is_equal_to(status.HTTP_404_NOT_FOUND)

    def test_should_delete_recipe_without_ingredients(self) -> None:
        recipe = RecipeFactory(ingredients=None)

        response = self.client.delete(f'/recipes/{recipe.id}')
        assert_that(response.status_code).is_equal_to(status.HTTP_204_NO_CONTENT)
        assert_that(Recipe.objects.all()).is_length(0)

    def test_should_delete_recipe_with_ingredients(self) -> None:
        recipe = RecipeFactory(
            ingredients=factory.RelatedFactoryList(IngredientFactory, factory_related_name='recipe', size=LIST_SIZE)
        )

        response = self.client.delete(f'/recipes/{recipe.id}')
        assert_that(response.status_code).is_equal_to(status.HTTP_204_NO_CONTENT)
        assert_that(Recipe.objects.all()).is_length(0)
        assert_that(Ingredient.objects.all()).is_length(0)
