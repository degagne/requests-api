import json
import simplejson
import requests

from requests import Session
from typing import NoReturn, Union, Optional, TextIO
from requests_api.constants import (
    STATUS_CODES,
    GET,
    HEAD,
    POST,
    PUT,
    DELETE,
    PATCH,
)
from requests_api.errors import RequestError
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
        auth: Union[HTTPBasicAuth, HTTPDigestAuth, OAuth2, HttpNtlmAuth, HTTPKerberosAuth],
        verify: Optional[Union[bool, TextIO]] = False,
        schema: Optional[str] = "https",
        headers: Optional[dict] = {"Content-type": "application/json"},
        allow_redirects: Optional[bool] = False
    ) -> NoReturn:
        """ initialize class """
        self.baseurl = baseurl
        self.auth = auth
        self.verify = verify
        self.schema = schema
        self.headers = headers
        self.allow_redirects = allow_redirects

    def encode_url(self, path: str, query_params: dict) -> str:
        """ encode url """
        return urlunsplit((self.schema, self.baseurl, path, urlencode(query_params), ""))

    def expected_status_code(self, http_method: str) -> list:
        """ sets expected status codes based on method type """
        status_codes = [200]
        with suppress(KeyError):
            status_codes = STATUS_CODES[http_method]
        return status_codes

    def get(
        self,
        path: str,
        query_params: Optional[dict] = {},
        search_keys: Optional[list] = [],
        status_codes: Optional[list] = [200]
    ):
        """ helper method for get request """
        return self.request(
            method="GET", 
            path=path, 
            query_params=query_params, 
            search_keys=search_keys,
            status_codes=status_codes
        )

    def head(
        self,
        path: str,
        query_params: Optional[dict] = {},
        search_keys: Optional[list] = [],
        status_codes: Optional[list] = [200]
    ):
        """ helper method for head request """
        return self.request(
            method="HEAD", 
            path=path, 
            query_params=query_params, 
            search_keys=search_keys,
            status_codes=status_codes
        )

    def post(
        self,
        path: str,
        query_params: Optional[dict] = {},
        request_data: Optional[dict] = {},
        search_keys: Optional[list] = [],
        status_codes: Optional[list] = [200, 201, 204]
    ):
        """ helper method for post request """
        return self.request(
            method="POST", 
            path=path, 
            query_params=query_params,
            request_data=request_data,
            search_keys=search_keys,
            status_codes=status_codes
        )

    def put(
        self,
        path: str,
        query_params: Optional[dict] = {},
        request_data: Optional[dict] = {},
        search_keys: Optional[list] = [],
        status_codes: Optional[list] = [200, 202, 204]
    ):
        """ helper method for put request """
        return self.request(
            method="PUT", 
            path=path, 
            query_params=query_params,
            request_data=request_data,
            search_keys=search_keys,
            status_codes=status_codes
        )

    def delete(
        self,
        path: str,
        query_params: Optional[dict] = {},
        search_keys: Optional[list] = [],
        status_codes: Optional[list] = [200, 202, 204]
    ):
        """ helper method for delete request """
        return self.request(
            method="DELETE", 
            path=path, 
            query_params=query_params,
            search_keys=search_keys,
            status_codes=status_codes
        )

    def patch(
        self,
        path: str,
        query_params: Optional[dict] = {},
        request_data: Optional[dict] = {},
        search_keys: Optional[list] = [],
        status_codes: Optional[list] = [200, 204]
    ):
        """ helper method for patch request """
        return self.request(
            method="PATCH", 
            path=path, 
            query_params=query_params,
            request_data=request_data,
            search_keys=search_keys,
            status_codes=status_codes
        )

    def request(
        self,
        method: str,
        path: str,
        query_params: Optional[dict] = {},
        request_data: Optional[dict] = {},
        search_keys: Optional[list] = [],
        status_codes: Optional[list] = None
    ) -> Union[bool, str]:
        """ submits http request """

        http_method = method.upper()

        session = Session()
        session.auth = self.auth
        session.verify = self.verify
        session.headers = self.headers
        session.allow_redirects = self.allow_redirects

        encoded_url = self.encode_url(path, query_params)

        try:
            if GET == http_method:
                response = session.get(encoded_url)
            elif HEAD == http_method:
                response = session.head(encoded_url)
            elif POST == http_method:
                response = session.post(encoded_url, data=json.dumps(request_data))
            elif PUT == http_method:
                response = session.put(encoded_url, data=json.dumps(request_data))
            elif DELETE == http_method:
                response = session.delete(encoded_url)
            elif PATCH == http_method:
                response = session.patch(encoded_url, data=json.dumps(request_data))
            else:
                raise RequestError(f"HTTP method type '{http_method}' is not supported.")
    
            # raise exception for error codes 4xx or 5xx
            response.raise_for_status()
        except (requests.exceptions.HTTPError,
                requests.ConnectionError,
                requests.Timeout,
                requests.exceptions.RequestException) as exception:
            message = getattr(exception, "message")
            raise RequestError(message.strip(), response.status_code)
        finally:
            session.close()

        # get list of expected status codes, otherwise override 
        # with provided codes
        expected_status_codes = (self.expected_status_code(http_method) if status_codes is None else status_codes)

        # check if status code returned is "expected", otherwise 
        # raise ``HTTPError``
        if response.status_code not in expected_status_codes:
            raise RequestError(f"Unexpected HTTP status code '{response.status_code}' returned with "
                               f"reason '{response.reason}'")

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
