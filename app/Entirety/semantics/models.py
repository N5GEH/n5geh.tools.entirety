from django.db import models

# Create your models here.
class Prefix(models.Model):
    name = models.CharField(max_length=200)
    value = models.CharField(max_length=200)
    projectid = models.CharField(max_length=200)
    key = models.CharField(max_length=200, primary_key=True)
    include = models.BooleanField(default=True)
    def __str__(self):
      return self.name