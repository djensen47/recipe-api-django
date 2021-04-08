from django.test import TestCase
from assertpy import assert_that
from rest_framework import status
from rest_framework.test import APIClient
from .factories import RecipeFactory, IngredientFactory
from ..models import Recipe
from ..serializers import RecipeSerializer
import factory

LIST_SIZE = 3


class RecipeUpdateTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.client = APIClient()

    def test_should_update_recipe_without_ingredients(self) -> None:
        recipe = RecipeFactory(ingredients=None)
        data = RecipeSerializer(recipe).data

        response = self.client.put(f'/recipes/{recipe.id}', data, format='json')
        db_recipe = Recipe.objects.get(id=response.data['id'])
        db_data = RecipeSerializer(db_recipe).data

        assert_that(response.status_code).is_equal_to(status.HTTP_200_OK)
        assert_that(db_data).is_equal_to(data)

    def test_should_update_recipe_with_ingredients(self) -> None:
        recipe = RecipeFactory(
            ingredients=factory.RelatedFactoryList(IngredientFactory, factory_related_name='recipe', size=LIST_SIZE)
        )
        data = RecipeSerializer(recipe).data

        response = self.client.put(f'/recipes/{recipe.id}', data, format='json')
        db_recipe = Recipe.objects.get(id=response.data['id'])
        db_data = RecipeSerializer(db_recipe).data

        assert_that(response.status_code).is_equal_to(status.HTTP_200_OK)
        assert_that(db_data).is_equal_to(data)

    def test_should_return_404(self) -> None:
        response = self.client.put(f'/recipes/1000', {}, format='json')
        assert_that(response.status_code).is_equal_to(status.HTTP_404_NOT_FOUND)

    def test_should_return_400_when_missing_required_field(self) -> None:
        recipe = RecipeFactory(ingredients=None)
        data = RecipeSerializer(recipe).data
        del data['name']

        response = self.client.put(f'/recipes/{recipe.id}', data, format='json')
        assert_that(response.status_code).is_equal_to(status.HTTP_400_BAD_REQUEST)

    def test_should_return_400_when_sent_extra_fields(self) -> None:
        recipe = RecipeFactory(ingredients=None)
        data = RecipeSerializer(recipe).data
        data['foo'] = 'bar'

        response = self.client.put(f'/recipes/{recipe.id}', data, format='json')
        assert_that(response.status_code).is_equal_to(status.HTTP_400_BAD_REQUEST)
