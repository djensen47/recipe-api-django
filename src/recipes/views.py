from random import random

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.decorators import action

from .models import Recipe
from .serializers import RecipeSerializer


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
    Endpoints for listing, creating, viewing, updating, and deleting recipes.

    If you need some inspiration for recipes, try [The Spruce Eats](https://www.thespruceeats.com/)
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    # Note, this method is unnecessary. It's here as an example.
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

