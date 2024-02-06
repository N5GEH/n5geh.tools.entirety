from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email")}),
        ("Permissions",
         {
             "fields": (
                 "is_active",
                 "is_staff",
                 "is_superuser",
                 "is_server_admin",
                 "is_project_admin"
             ),
         },
         ),
    )


# Register your models here.
if settings.LOCAL_AUTH:
    admin.site.register(User, CustomAdmin)
