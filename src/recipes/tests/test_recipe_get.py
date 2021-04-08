from django.test import TestCase
from assertpy import assert_that
from rest_framework import status
from rest_framework.test import APIClient
from .factories import RecipeFactory, IngredientFactory
from ..serializers import RecipeSerializer
import factory

LIST_SIZE = 3


class RecipeGetTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.api_client = APIClient()

    def test_should_return_recipe_with_no_ingredients(self) -> None:
        recipe = RecipeFactory(ingredients=None)
        serialized_recipe = RecipeSerializer(recipe).data

        response = self.api_client.get(f'/recipes/{recipe.id}')
        data = response.data
        assert_that(response.status_code).is_equal_to(status.HTTP_200_OK)
        assert_that(data).is_equal_to(serialized_recipe)

    def test_should_return_recipe_with_ingredients(self) -> None:
        recipe = RecipeFactory(
            ingredients=factory.RelatedFactoryList(IngredientFactory, factory_related_name='recipe', size=LIST_SIZE)
        )
        serialized_recipe = RecipeSerializer(recipe).data

        response = self.api_client.get(f'/recipes/{recipe.id}')
        data = response.data
        assert_that(response.status_code).is_equal_to(status.HTTP_200_OK)
        assert_that(data).is_equal_to(serialized_recipe)

    def test_should_return_404(self) -> None:
        response = self.api_client.get(f'/recipes/1000')
        assert_that(response.status_code).is_equal_to(status.HTTP_404_NOT_FOUND)
