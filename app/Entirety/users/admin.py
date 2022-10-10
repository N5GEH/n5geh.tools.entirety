from django.conf import settings
from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    exclude = ["groups", "user_permissions"]


# Register your models here.
if settings.LOCAL_AUTH:
    admin.site.register(User, UserAdmin)
