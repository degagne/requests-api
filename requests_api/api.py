import json
import logging
import requests
import urllib3
import typing as t

from requests.auth import HTTPBasicAuth, HTTPDigestAuth
from requests_oauthlib import OAuth2
from requests_ntlm3 import HttpNtlmAuth
from requests_kerberos import HTTPKerberosAuth
from urllib.parse import urlunsplit, urlencode
from nested_lookup import nested_lookup

from requests_api.adapter import RetryAdapter
from requests_api.exception import HTTPError


urllib3.disable_warnings() # Disable `Insecure Request` warnings

logging.basicConfig(level=logging.DEBUG)
LOG = logging.getLogger(__name__)


class RequestsAPI:

    def __init__(
        self,
        baseurl: str, 
        auth: t.Union[HTTPBasicAuth, HTTPDigestAuth, OAuth2, HttpNtlmAuth, HTTPKerberosAuth],
        verify: t.Optional[t.Union[bool, t.TextIO]] = False,
        retry: t.Optional[t.Type[RetryAdapter]] = RetryAdapter,
        schema: t.Optional[str] = "https",
        headers: t.Optional[t.Dict[str, t.Any]] = {"Content-type": "application/json"},
        allow_redirects: t.Optional[bool] = False
    ) -> t.NoReturn:

        self.baseurl = baseurl
        self.auth = auth
        self.verify = verify
        self.retry = retry
        self.schema = schema
        self.headers = headers
        self.allow_redirects = allow_redirects

    def request_encode_url(self, path: str, query_params: t.Dict[str, t.Any]) -> str:
        """
        Returns URI for execution with query parameters.

        :param path: URI base path
        :param query_params: URI query parameters
        :return: A URI with encoded parameters.
        """
        return urlunsplit((self.schema, self.baseurl, path, urlencode(query_params), ""))

    def request_expected_status_code(self, method: str) -> t.List[t.Any]:
        """Sets expected HTTP status codes for each HTTP method invoked.

        These expected HTTP status codes can be overridden, by including the 
        ``status_code`` argument for the ``request`` method.

        See https://www.w3.org/Protocols/rfc2616/rfc2616-sec9.html for additional information.

        :param str method: HTTP method such as GET, POST, PUT, etc.
        :return: A list of status codes to allow as "accepted".
        """
        if method.upper() == "GET":
            return [200]
        if method.upper() == "HEAD":
            return [200]
        if method.upper() == "POST":
            return [200, 201, 204]
        if method.upper() == "PUT":
            return [200, 202, 204]
        if method.upper() == "DELETE":
            return [200, 202, 204]
        if method.upper() == "PATCH":
            return [200, 204]

    def submit_request(
        self,
        method: str,
        path: str,
        query_params: t.Optional[t.Dict[str, t.Any]] = {},
        request_data: t.Optional[t.Dict[str, t.Any]] = {},
        status_codes: t.Optional[t.List[int]] = None
    ) -> t.Union[bool, str]:
        """Submits HTTP request.

        :param method: HTTP method such as GET, POST, PUT, etc.
        :param path: Path URL to be appended to the base URL.
        :param query_params: Optional. Query parameters to encode to append to our URL. 
            Generally used for GET methods.
        :param request_data: Optional. Data to send in the body of the request. This is reserved 
            for POST, PUT or PATCH methods only.
        :param status_codes: Optional. List of status codes to define a "successful" request 
            attempt. By default these are set by the ``request_expected_status_code``
            method, however, they can be overridden.
        :raises: ``.HTTPError`` -- if an error is returned
        :return: JSON string with request response, otherwise False.
        """
        session = requests.Session()
        session.auth = self.auth
        session.verify = self.verify
        session.headers = self.headers
        session.allow_redirects = self.allow_redirects

        encoded_url = self.request_encode_url(path, query_params)

        session.mount(encoded_url, self.retry(max_retries=5))

        try:
            if "GET" == method.upper():
                response = session.get(encoded_url)
            if "HEAD" == method.upper():
                response = session.head(encoded_url)
            if "POST" == method.upper():
                response = session.post(encoded_url, data=json.dumps(request_data))
            if "PUT" == method.upper():
                response = session.put(encoded_url, data=json.dumps(request_data))
            if "DELETE" == method.upper():
                response = session.delete(encoded_url)
            if "PATCH" == method.upper():
                response = session.patch(encoded_url, data=json.dumps(request_data))

            # Raise exception for all error codes (4xx or 5xx)
            response.raise_for_status()
        except (requests.exceptions.HTTPError,
                requests.ConnectionError,
                requests.Timeout,
                requests.exceptions.RequestException) as exception:
            raise HTTPError(getattr(exception, 'message', repr(exception)))
        finally:
            session.close()

        # Get list of expected status codes, otherwise override with 
        # provided codes.
        expected_status_codes = (
            self.request_expected_status_code(method) if status_codes is None else status_codes
        )

        # Check if status code returned is "expected", otherwise 
        # raise `HTTPError`.
        if response.status_code not in expected_status_codes:
            raise HTTPError(f"Unexpected HTTP status code '{response.status_code}' "
                            f"returned with reason '{response.reason}'")

        # For responses with no content, return True to indicate that
        # the HTTP request was successful.
        if not response.content:
            return True

        try:
            return response.json()
        except json.JSONDecodeError as exception:
            pass # not a JSON serialized data stream
        return response.text
