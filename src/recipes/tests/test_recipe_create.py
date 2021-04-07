from django.test import TestCase
from assertpy import assert_that
from rest_framework import status
from rest_framework.test import APIClient
from .factories import RecipeFactory, IngredientFactory
from ..models import Recipe
from ..serializers import RecipeSerializer
import factory

LIST_SIZE = 3


class RecipeCreateTestCase(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_should_create_recipe_without_ingredients(self) -> None:
        # use .build() so that we don't persist to the database
        recipe = RecipeFactory.build(ingredients=None)
        data = RecipeSerializer(recipe).data
        del data['id']

        response = self.client.post('/recipes', data, format='json')
        db_recipe = Recipe.objects.get(id=response.data['id'])
        db_data = RecipeSerializer(db_recipe).data
        del db_data['id']

        assert_that(response.status_code).is_equal_to(status.HTTP_201_CREATED)
        assert_that(db_data).is_equal_to(data)

    def test_should_create_recipe_with_ingredients(self) -> None:
        # use .build() so that we don't persist to the database
        recipe = RecipeFactory.build(
            ingredients=factory.RelatedFactoryList(IngredientFactory, factory_related_name='recipe', size=LIST_SIZE)
        )
        data = RecipeSerializer(recipe).data
        del data['id']

        response = self.client.post('/recipes', data, format='json')
        db_recipe = Recipe.objects.get(id=response.data['id'])
        db_data = RecipeSerializer(db_recipe).data
        del db_data['id']

        assert_that(response.status_code).is_equal_to(status.HTTP_201_CREATED)
        assert_that(db_data).is_equal_to(data)

    def test_should_return_400_when_missing_required_field(self) -> None:
        recipe = RecipeFactory.build(ingredients=None)
        data = RecipeSerializer(recipe).data
        del data['id']
        del data['name']

        response = self.client.post('/recipes', data, format='json')
        assert_that(response.status_code).is_equal_to(status.HTTP_400_BAD_REQUEST)

    def test_should_return_400_when_sent_extra_fields(self) -> None:
        recipe = RecipeFactory.build(ingredients=None)
        data = RecipeSerializer(recipe).data
        data['foo'] = 'bar'
        del data['id']

        response = self.client.post('/recipes', data, format='json')
        assert_that(response.status_code).is_equal_to(status.HTTP_400_BAD_REQUEST)
