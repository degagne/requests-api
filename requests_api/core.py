import json
import simplejson
import requests

from requests import Session
from typing import NoReturn, Union, Optional, TextIO, Type, Dict, Any, List
from requests_api.constants import (
    HEADERS,
    STATUS_CODES,
    GET,
    HEAD,
    POST,
    PUT,
    DELETE,
    PATCH,
    MAX_RETRIES,
    SCHEMA
)
from requests_api.errors import RequestError
from requests_api.adapter import RetryAdapter
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
from requests_oauthlib import OAuth2
from requests_ntlm3 import HttpNtlmAuth
from requests_kerberos import HTTPKerberosAuth
from urllib.parse import urlunsplit, urlencode
from contextlib import suppress
from nested_lookup import nested_lookup


class Requests:

    def __init__(
        self,
        baseurl: str,
        auth: Union[HTTPBasicAuth, HTTPDigestAuth, OAuth2, HttpNtlmAuth, 
                    HTTPKerberosAuth],
        verify: Optional[Union[bool, TextIO]] = False,
        retries: Optional[Type[RetryAdapter]] = RetryAdapter(max_retries=MAX_RETRIES),
        schema: Optional[str] = SCHEMA,
        headers: Optional[Dict[str, str]] = HEADERS,
        allow_redirects: Optional[bool] = False
    ) -> NoReturn:
        """ initialize class """
        self.baseurl = baseurl
        self.auth = auth
        self.verify = verify
        self.retries = retries
        self.schema = schema
        self.headers = headers
        self.allow_redirects = allow_redirects

    def encode_url(self, path: str, query_params: Dict[str, Any]) -> str:
        """ generates uri for execution with query parameters """
        query_params = urlencode(query_params)
        return urlunsplit((self.schema, self.baseurl, path, query_params, ""))

    def expected_status_code(self, method_name: str) -> List[int]:
        """ sets expected status codes based on method type """
        status_codes = [200]
        with suppress(KeyError):
            status_codes = STATUS_CODES[method_name.upper()]
        return status_codes

    def request(
        self,
        method: str,
        path: str,
        query_params: Optional[Dict[str, Any]] = {},
        request_data: Optional[Dict[str, Any]] = {},
        search_keys: Optional[List[str]] = [],
        status_codes: Optional[List[int]] = None
    ) -> Union[bool, str]:
        """ submits http request """
        if method.upper() not in STATUS_CODES.keys():
            raise RequestError(f"Unsupported method type: {method.upper()}")

        session = Session()
        session.auth = self.auth
        session.verify = self.verify
        session.headers = self.headers
        session.allow_redirects = self.allow_redirects

        encoded_url = self.encode_url(path, query_params)

        session.mount(encoded_url, self.retries)

        try:
            if GET == method.upper():
                response = session.get(encoded_url)
            if HEAD == method.upper():
                response = session.head(encoded_url)
            if POST == method.upper():
                response = session.post(encoded_url, data=json.dumps(request_data))
            if PUT == method.upper():
                response = session.put(encoded_url, data=json.dumps(request_data))
            if DELETE == method.upper():
                response = session.delete(encoded_url)
            if PATCH == method.upper():
                response = session.patch(encoded_url, data=json.dumps(request_data))

            # raise exception for error codes 4xx or 5xx
            response.raise_for_status()
        except (requests.exceptions.HTTPError,
                requests.ConnectionError,
                requests.Timeout,
                requests.exceptions.RequestException) as exception:
            raise RequestError(getattr(exception, "message", repr(exception)))
        finally:
            session.close()

        # get list of expected status codes, otherwise override 
        # with provided codes
        expected_status_codes = (
            self.expected_status_code(method) 
                if status_codes is None else status_codes)

        # check if status code returned is "expected", otherwise 
        # raise ``HTTPError``
        if response.status_code not in expected_status_codes:
            raise RequestError(
                f"Unexpected HTTP status code '{response.status_code}' "
                f"returned with reason '{response.reason}'")

        # for responses with no content, return True to indicate 
        # that the request was successful
        if not response.content:
            return True

        with suppress(json.JSONDecodeError, simplejson.JSONDecodeError):
            response = response.json()
            if not search_keys:
                return response
            results = [nested_lookup(key, response) for key in search_keys]
            return [item for sublist in results for item in sublist]
        return response.text
