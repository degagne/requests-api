from __future__ import absolute_import

from typing import List, Dict, NoReturn, Any
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from requests_api.constants import (
    BACKOFF_FACTOR,
    STATUS_FORCELIST,
    ALLOWED_METHODS
)


class RetryAdapter(HTTPAdapter):
    """ creates retry adapter to allow for retries """

    def __init__(self, *args: List[Any], **kwargs: Dict[str, Any]) -> NoReturn:
        """ class constructor """
        super().__init__(*args, **kwargs)
        self.max_retries = Retry(
            total=self.max_retries,
            backoff_factor=BACKOFF_FACTOR,
            status_forcelist=STATUS_FORCELIST,
            allowed_methods=ALLOWED_METHODS)
