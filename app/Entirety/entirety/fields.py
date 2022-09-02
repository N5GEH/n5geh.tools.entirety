from django.core.validators import URLValidator
from django.forms import MultiValueField, ChoiceField, CharField, URLField
from django.utils.translation import gettext_lazy as _

from entirety.widgets import SelectTextInputWidget
from entirety.validators import CustomURLValidator


class MQTTURLField(URLField):
    """URL Field that accepts URLs that start with mqtt:// only"""

    default_validators = [CustomURLValidator(schemes=["mqtt"])]
    default_error_messages = {
        "invalid": _("Enter a valid MQTT URL."),
    }


class HTTPURLField(URLField):
    """URL Field that accepts URLs that start with http(s):// only"""

    default_validators = [CustomURLValidator(schemes=["http", "https"])]
    default_error_messages = {
        "invalid": _("Enter a valid URL."),
    }


class SelectTextMultiField(MultiValueField):
    def __init__(self, choices, *, require_all_fields=True, **kwargs):
        self.widget = SelectTextInputWidget(choices)
        fields = (
            ChoiceField(
                choices=choices,
            ),
            CharField(),
        )
        super(SelectTextMultiField, self).__init__(
            fields=fields, require_all_fields=require_all_fields, **kwargs
        )

    def compress(self, data_list):
        if data_list:
            return "|".join(data_list)

        return ""
