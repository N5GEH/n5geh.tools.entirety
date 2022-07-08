from django.db import models

from users.models import User
from utils.generators import generate_uuid


class Project(models.Model):
    uuid = models.CharField(
        unique=True, max_length=64, default=generate_uuid, primary_key=True
    )
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=300, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    fiware_service = models.CharField(max_length=64, null=True)
    fiware_service_path = models.CharField(max_length=1, default="/", null=True)

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name="users")

    def is_owner(self, user: User):
        return self.owner == user

    def is_user(self, user: User):
        return user in self.users

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
