from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, viewsets
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from .models import Recipe, Ingredient
from .serializers import RecipeSerializer, IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """
    Returns a list of recipes _with_ their **ingredients**.

    For more details, [Learn to Cook](http://google.com)
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class IngredientList(APIView):
    """" List or create ingredients"""

    def get(self, request: Request, format=None) -> Response:
        ingredients = Ingredient.objects.all()
        serializer = IngredientSerializer(ingredients, many=True)
        return Response(serializer.data)
