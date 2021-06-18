import json
import requests
import urllib3

from typing import NoReturn, TextIO, Union, Type, Dict, Any, Optional, List

from requests.auth import HTTPBasicAuth, HTTPDigestAuth
from requests.adapters import HTTPAdapter
from requests_oauthlib import OAuth2
from requests_ntlm3 import HttpNtlmAuth
from requests_kerberos import HTTPKerberosAuth
from urllib.parse import urlunsplit, urlencode

from requests_api.retries import Retries
from requests_api.exception import HTTPError


urllib3.disable_warnings() # Disable `Insecure Request` warnings


class RequestsAPI:

    def __init__(
        self,
        baseurl: str, 
        auth: Union[HTTPBasicAuth, HTTPDigestAuth, OAuth2, HttpNtlmAuth, HTTPKerberosAuth],
        verify: Optional[Union[bool, TextIO]] = False,
        retries: Optional[Type[Retries]] = Retries,
        schema: Optional[str] = "https",
        headers: Optional[Dict[str, Any]] = {"Content-type": "application/json"},
        allow_redirects: Optional[bool] = False
    ) -> NoReturn:

        self.baseurl = baseurl
        self.auth = auth
        self.verify = verify
        self.retries = retries
        self.schema = schema
        self.headers = headers
        self.allow_redirects = allow_redirects

    def request_encode_url(self, path: str, query_params: Dict[str, Any]) -> str:
        return urlunsplit((self.schema, self.baseurl, path, urlencode(query_params), ""))

    def request_expected_status_code(self, method: str) -> list:
        """
        Sets expected HTTP status codes for each HTTP method invoked.

        These expected HTTP status codes can be overridden, by including
        the ``status_code`` parameter when invoking the ``request`` method.

        See https://www.w3.org/Protocols/rfc2616/rfc2616-sec9.html for 
        additional information.

        :param method:
            HTTP method such as GET, POST, PUT, etc.
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

    def request(
        self,
        method: str,
        path: str,
        query_params: Optional[Dict[str, Any]] = {},
        request_data: Optional[Dict[str, Any]] = {},
        status_codes: Optional[List[int]] = None
    ) -> bool:
        """
        Submits HTTP request.

        :param method:
            HTTP method such as GET, POST, PUT, etc.

        :param path:
            Path URL to be appended to the base URL.

        :param query_params:
            Optional. Query parameters to encode to append to our URL. Generally
            used for GET methods.

        :param request_data:
            Optional. Data to send in the body of the request. This is reserved
            for POST, PUT or PATCH methods only.

        :param status_codes:
            Optional. List of status codes to define a "successful" request
            attempt. By default these are set by the ``request_expected_status_code``
            method, however, they can be overridden.
        """

        session = requests.Session()
        session.auth = self.auth
        session.verify = self.verify
        session.headers = self.headers
        session.allow_redirects = self.allow_redirects

        path = self.request_encode_url(path, query_params)

        session.mount(path, HTTPAdapter(max_retries=self.retries))

        try:
            if "GET" == method.upper():
                response = session.get(path)
            if "HEAD" == method.upper():
                response = session.head(path)
            if "POST" == method.upper():
                response = session.post(path, data=json.dumps(request_data))
            if "PUT" == method.upper():
                response = session.put(path, data=json.dumps(request_data))
            if "DELETE" == method.upper():
                response = session.delete(path)
            if "PATCH" == method.upper():
                response = session.patch(path, data=json.dumps(request_data))

            # Raise exception for all error codes (4xx or 5xx)
            response.raise_for_status()

        except (requests.exceptions.HTTPError,
                requests.ConnectionError,
                requests.Timeout,
                requests.exceptions.RequestException
        ) as exception:
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
