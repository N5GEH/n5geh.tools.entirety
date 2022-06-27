from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class ExampleModel(models.Model):

    title = models.CharField(max_length=40, unique=True)

    year = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1895), MaxValueValidator(2050)]
    )
