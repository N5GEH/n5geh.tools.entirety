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
