import factory


class IngredientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'recipes.Ingredient'
        django_get_or_create = ('name',)

    name = factory.Sequence(lambda n: 'cheese %d' % n)
    # name = 'cheese'


class RecipeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'recipes.Recipe'
        django_get_or_create = ('name', 'description',)

    # name = 'Pizze'
    name = factory.Sequence(lambda n: 'Pizza %d' % n)
    description = 'A recipe to create the most perfect food.'
    # ingredients = factory.RelatedFactory(IngredientFactory, factory_related_name='recipe')
    ingredients = factory.RelatedFactoryList(IngredientFactory, factory_related_name='recipe', size=3)

