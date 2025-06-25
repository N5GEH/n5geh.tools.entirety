from django import forms
from django.contrib.auth.forms import UserCreationForm

from users.models import User

# from crispy_forms.helper import FormHelper


class UserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for x, field in self.fields.items():
            field.disabled = True
        # self.helper = FormHelper()
        # self.helper.form_tag = False
        # self.helper.field_class = "col-lg-2"

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "is_superuser",
            "is_server_admin",
            "is_project_admin",
        ]


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        )
