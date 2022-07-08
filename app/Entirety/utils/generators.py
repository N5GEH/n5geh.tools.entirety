from secrets import token_urlsafe
from uuid import uuid4


def generate_uuid():
    return str(uuid4())


def generate_secret_key(length: int = 64) -> str:
    return token_urlsafe(length)
