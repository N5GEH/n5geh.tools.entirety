from django.db import models
from django_resized import ResizedImageField
from users.models import User
from utils.generators import generate_uuid


class Project(models.Model):
    uuid = models.CharField(
        unique=True, max_length=64, default=generate_uuid, primary_key=True
    )
    name = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=300, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    fiware_service = models.CharField(max_length=64, null=True)
    fiware_service_path = models.CharField(max_length=1, default="/", null=True)
    webpage_url = models.URLField(max_length=200, null=True)
    dashboard_url = models.URLField(max_length=200, null=True)
    logo = ResizedImageField(
        size=[160, 150], crop=["middle", "center"], upload_to="images/", null=True
    )

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name="users", blank=True)
    maintainers = models.ManyToManyField(User, related_name="maintainers", blank=True)
    viewers = models.ManyToManyField(User, related_name="viewers", blank=True)

    is_viewer_public = models.BooleanField(
        default=False,
        help_text="If enabled, all users (including future ones) have viewer access.",
    )
    is_user_public = models.BooleanField(
        default=False,
        help_text="If enabled, all users (including future ones) have user access.",
    )
    is_maintainer_public = models.BooleanField(
        default=False,
        help_text="If enabled, all users (including future ones) have maintainer access.",
    )

    def is_owner(self, user: User):
        return self.owner == user

    def is_user(self, user: User):
        return self.is_user_public or user in self.users.all()

    def is_maintainer(self, user: User):
        return self.is_maintainer_public or user in self.maintainers.all()

    def is_viewer(self, user: User):
        return self.is_viewer_public or user in self.viewers.all()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
