from django import forms
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
