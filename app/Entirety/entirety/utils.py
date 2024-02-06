from django.utils.html import format_html


def pop_data_from_session(request, key):
    """
    Pop data from session
    """
    if request.session.get(key):
        return request.session.pop(key)
    else:
        return None


def add_data_to_session(request, key, value):
    """
    Add data to session
    """
    request.session[key] = value
    return request


def django_table2_limit_text_length(value,
                                    length: int = None):
    """
    Limit the length of a column in django-table2.

    Example
    ---
    class DevicesTable(tables.Table):
        ...
        device_id = tables.columns.Column()
        ...
        def render_device_id(self, value):
            length_limit = 20
            return django_table2_limit_text_length(value, length=length_limit)
    """
    if length is None:
        length = 20
    truncated_value = value[:length] + '...' if len(value) > length else value
    return format_html('<span title="{}">{}</span>', value, truncated_value)
