from django import forms


class SelectTextInputWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        widgets = (
            forms.TextInput(attrs=attrs),
            forms.TextInput(attrs=attrs),
        )
        super(SelectTextInputWidget, self).__init__(widgets, attrs)
