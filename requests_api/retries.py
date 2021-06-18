from typing import Any, Dict, NoReturn, Optional
from urllib3.util.retry import Retry

from requests_api.exception import RequestsAPIConfigurationError


class Retries(Retry):
    """
    This class provides the logic to retry http requests from the 'requests'
    session object.
    """
    DEFAULT_CONFIG = {
        "total": 5,
        "connect": 0,
        "read": 0,
        "redirect": 0,
        "status": 0,
        "other": 0,
        "allowed_methods": frozenset({"DELETE", "GET", "PUT", "POST"}),
        "status_forcelist": [500, 502, 503, 504],
        "backoff_factor": 0.1,
        "raise_on_redirect": True,
        "raise_on_status": True,
        "history": None,
        "respect_retry_after_header": True,
        "remove_headers_on_redirect": frozenset({"Authorization"})
    }

    def __init__(self, **configs: Optional[Dict[str, Any]]) -> NoReturn:
        invalid_configs = set(configs).difference(self.DEFAULT_CONFIG)
        if invalid_configs:
            raise RequestsAPIConfigurationError(f"Invalid configuration properties: {invalid_configs}")
        new_configs = self.DEFAULT_CONFIG
        new_configs.update(configs)

        super().__init__(**new_configs)