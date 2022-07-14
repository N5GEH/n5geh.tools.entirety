from uuid import uuid4

from django.db import models


def generate_uuid():
    return str(uuid4())


class Project(models.Model):
    uuid = models.CharField(unique=True, max_length=64,
                            default=generate_uuid, primary_key=True)
    name = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=300, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    fiware_service = models.CharField(max_length=64, null=True)
    fiware_service_path = models.CharField(max_length=1, default="/", null=True)
    webpage_url = models.URLField(max_length=200, null=True)
    logo = models.ImageField(upload_to='images/', null=True)

    def __str__(self):
        return self.name




