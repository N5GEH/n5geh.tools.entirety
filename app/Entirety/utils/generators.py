from secrets import token_urlsafe


def generate_secret_key(length: int = 64) -> str:
    return token_urlsafe(length)
