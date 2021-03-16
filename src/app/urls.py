"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.renderers import JSONOpenAPIRenderer, OpenAPIRenderer
from rest_framework.schemas import get_schema_view

title = "Recipes API"
version = "1.0.0"

# TODO: if you can specify multiple renderers, shouldn't there be a way to re-use the result of get_schema_view?
schema_json = get_schema_view(
    title=title,
    version=version,
    renderer_classes=[JSONOpenAPIRenderer],
)

schema_yaml = get_schema_view(
    title=title,
    version=version,
    renderer_classes=[OpenAPIRenderer],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('recipes.urls')),
    path('schema.json', schema_json),
    path('schema.yaml', schema_yaml, name='openapi-schema'),
    path('docs/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url': 'openapi-schema'}
    ))
    # path('', recipes.urls)
]
