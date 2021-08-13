import typing as t

from requests_api import RequestsAPI
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
from requests_oauthlib import OAuth2
from requests_ntlm3 import HttpNtlmAuth
from requests_kerberos import HTTPKerberosAuth
from nested_lookup import nested_lookup
from requests_api.exception import HTTPError

from requests_api.adapter import RetryAdapter


class pass_requests(RequestsAPI):
    """
    Request decorator with a search functionality to find specific
    keys from our response.

    :param search_keys:
        Optional. List of keys to search our JSON object for.
    """
    def __init__(
        self,
        baseurl: str, 
        auth: t.Union[HTTPBasicAuth, HTTPDigestAuth, OAuth2, HttpNtlmAuth, HTTPKerberosAuth],
        verify: t.Optional[t.Union[bool, t.TextIO]] = False,
        retries: t.Optional[t.Type[RetryAdapter]] = RetryAdapter,
        schema: t.Optional[str] = "https",
        headers: t.Optional[t.Dict[str, t.Any]] = {"Content-type": "application/json"},
        allow_redirects: t.Optional[bool] = False
    ) -> t.NoReturn:
        super().__init__(baseurl, auth, verify, retries, schema, headers, allow_redirects)

    def request(
        self,
        method: str,
        path: str,
        search_keys: list,
        query_params: t.Optional[t.Dict[str, t.Any]] = {},
        request_data: t.Optional[t.Dict[str, t.Any]] = {},
        status_codes: t.Optional[t.List[int]] = None
    ):
        response = self.submit_request(method, path, query_params, request_data, status_codes)
        if isinstance(response, bool):
            return True # no content
        if isinstance(response, dict):
            if search_keys:
                results = list(map(lambda x: nested_lookup(x, response), search_keys))
                return [item for sublist in results for item in sublist]
            else:
                return response
        return response

    def __call__(self, func: t.Callable):
        def inner_function(*args: t.List[t.Any], **kwargs: t.Dict[str, t.Any]):
            try:
                return func(self, *args, **kwargs)
            except HTTPError:
                return False
        return inner_function