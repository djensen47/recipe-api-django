from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


router = DefaultRouter(trailing_slash=False)
router.register(r'recipes', views.RecipeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('ingredients', views.IngredientList.as_view()),
]

# urlpatterns = format_suffix_patterns(urlpatterns)
