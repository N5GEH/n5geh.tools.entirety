from django.urls import path

from users import views

urlpatterns = [path("", views.user_info, name="user")]
