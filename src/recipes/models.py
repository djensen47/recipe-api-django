from django.db import models


# Create your models here.
class Recipe(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=True)
