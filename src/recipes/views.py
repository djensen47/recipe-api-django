from random import random

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from .models import Recipe, Ingredient
from .serializers import RecipeSerializer, IngredientSerializer


@extend_schema_view(
    list=extend_schema(
        description='Example 1: Document the API at the class level.',
    ),
    partial_update=extend_schema(
        exclude=True,
        description='This will not be in the specs because we used the exclude option above.'
    ),

)
class RecipeViewSet(viewsets.ModelViewSet):
    """
    Returns a list of recipes _with_ their **ingredients**.

    For more details, [Learn to Cook](http://google.com)
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def create(self, request, *args, **kwargs):
        """
        Example 2: Document the API in a docstring. This option might be the most limiting.
        """
        return super().create(request, args, kwargs)

    @extend_schema(
        description='Return a _random_ recipe.\n'
                    '\n'
                    '**Note:** Does not use a cryptographically secure PRNG.'
    )
    @action(detail=False)
    def random(self):
        return random.choice(self.queryset)


class IngredientList(APIView):
    """" List or create ingredients"""

    def get(self, request: Request, format=None) -> Response:
        ingredients = Ingredient.objects.all()
        serializer = IngredientSerializer(ingredients, many=True)
        return Response(serializer.data)
