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


class DropdownOrTextWidget(forms.MultiWidget):
    def __init__(self, choices=[], tooltip="initial tooltips", **kwargs):
        attrs = {}
        pattern = None
        if "selector" in kwargs and kwargs["selector"] != None:
            if kwargs["selector"] == "pattern":
                if kwargs["pattern"] != None:
                    attrs["hidden"] = "hidden"
                    pattern = kwargs["pattern"]
            elif kwargs["selector"] == "id":
                attrs["initial"] = kwargs["id"]
            else:
                logger.error(f"Do not understand selector: {kwargs['selector']}")

        self.widgets = (
            forms.Select(
                choices=choices,
                attrs=attrs,
            ),
            forms.TextInput(
                attrs={
                    "data-bs-toggle": "tooltip",
                    "data-bs-placement": "top",
                    "title": tooltip,
                    "type": "hidden" if pattern == None else "text",
                    "value": pattern if pattern != None else "---",
                },
            ),
        )
        super(DropdownOrTextWidget, self).__init__(self.widgets)

    def decompress(self, value):
        return ["", ""]
