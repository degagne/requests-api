from __future__ import absolute_import

import typing as t

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class RetryAdapter(HTTPAdapter):

    def __init__(self, *args: t.List[t.Any], **kwargs: t.Dict[str, t.Any]) -> t.NoReturn:
        super().__init__(*args, **kwargs)
        status_forcelist = [500, 502, 503]
        allowed_methods = frozenset(["POST", "HEAD", "TRACE", "GET", "PUT", "OPTIONS", "DELETE"])
        self.max_retries = Retry(
            total=self.max_retries,
            backoff_factor=2,
            status_forcelist=status_forcelist,
            allowed_methods=allowed_methods
        )
