
from django.db import models

# This file is intentionally left mostly empty for debugging.
# We will add models back one by one.

class TestModel(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name