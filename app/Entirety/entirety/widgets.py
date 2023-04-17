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


class ListTextWidget(forms.TextInput):
    def __init__(self, data_list, name, *args, **kwargs):
        super(ListTextWidget, self).__init__(*args, **kwargs)
        self._name = name
        self._list = data_list
        self.attrs.update({"list": "list__%s" % self._name, "autocomplete": "off"})

    def render(self, name, value, attrs=None, renderer=None):
        text_html = super(ListTextWidget, self).render(name, value, attrs=attrs)
        data_list = '<datalist id="list__%s">' % self._name
        for item in self._list:
            data_list += '<option value="%s">' % item
        data_list += "</datalist>"

        return text_html + data_list
