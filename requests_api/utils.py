from typing import Any, Callable, Dict, List, NoReturn, Optional
from nested_lookup import nested_lookup
from requests_api.exception import HTTPError


class request_decorator:
    """
    Request decorator with a search functionality to find specific
    keys from our response.

    :param search_keys:
        Optional. List of keys to search our JSON object for.
    """
    def __init__(self, search_keys: Optional[List[Any]] = None) -> NoReturn:
        self._search_keys = search_keys

    def __call__(self, function: Callable):
        def inner_function(*args: List[Any], **kwargs: Dict[str, Any]):
            try:
                response = function(*args, **kwargs)
                if isinstance(response, bool):
                    return True # no content
                if isinstance(response, dict):
                    if self._search_keys:
                        results = list(map(lambda x: nested_lookup(x, response), self._search_keys))
                        return [item for sublist in results for item in sublist]
                    else:
                        return response
                return response
            except HTTPError:
                return False
        return inner_function
