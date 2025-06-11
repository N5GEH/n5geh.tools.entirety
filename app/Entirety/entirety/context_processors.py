from django.conf import settings


def logo_filename(request):
    return {"logo_filename": settings.LOGO_FILENAME}
