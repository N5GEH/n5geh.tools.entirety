from django import forms


class SelectTextInputWidget(forms.MultiWidget):
    template_name = "widgets/select_text.html"

    def __init__(self, choices=[], attrs=None):
        widgets = (
            forms.Select(
                choices=choices, attrs=attrs if attrs else {"class": "form-select"}
            ),
            forms.TextInput(attrs=attrs),
        )
        super(SelectTextInputWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        return ["", ""]
