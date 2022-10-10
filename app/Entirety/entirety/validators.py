import re

from django.core.validators import URLValidator
from django.utils.regex_helper import _lazy_re_compile


class CustomURLValidator(URLValidator):
    def __init__(self, schemes=None, **kwargs):
        super().__init__(schemes, **kwargs)
        self.host_re = (
            "("
            + self.hostname_re
            + "(?:"
            + self.domain_re
            + self.tld_re
            + ")?|localhost)"
        )
        self.regex = _lazy_re_compile(
            r"^(?:[a-z0-9.+-]*)://"  # scheme is validated separately
            r"(?:[^\s:@/]+(?::[^\s:@/]*)?@)?"  # user:pass authentication
            r"(?:" + self.ipv4_re + "|" + self.ipv6_re + "|" + self.host_re + ")"
            r"(?::\d{1,5})?"  # port
            r"(?:[/?#][^\s]*)?"  # resource path
            r"\Z",
            re.IGNORECASE,
        )
