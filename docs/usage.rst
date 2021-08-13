===============
Usage Overview
===============

Create an authentication object
================================

Supports:

- `HTTPBasicAuth <https://docs.python-requests.org/en/latest/api/#authentication>`_
- `HTTPDigestAuth <https://docs.python-requests.org/en/latest/api/#authentication>`_
- `OAuth2 <https://requests-oauthlib.readthedocs.io/en/latest/oauth2_workflow.html>`_
- `HttpNtlmAuth <https://pypi.org/project/requests-ntlm3/>`_
- `HTTPKerberosAuth <https://pypi.org/project/requests-kerberos/>`_

.. code-block:: python
    :caption: Python
    :linenos:

    from requests_api import basic_auth

    auth = basic_auth("username", "supersecurepassword")

Create ``RequestsAPI`` object
=============================

.. code-block:: python
    :caption: Python
    :linenos:
    
    from requests_api import RequestsAPI

    r = RequestsAPI("whatever.example.com", auth, retries=retries)
    response = r.request("GET", "some/api/path/here", query_params={"fields": "something"})
    
The ``RequestsAPI`` also has a decorator object which can simplify the process and search for keys within the response object.

.. code-block:: python
    :caption: Python

    from requests_api import pass_requests
    from requests_api import RequestsAPI
    from requests_api import basic_auth

    SCHEMA = "http"
    BASEURL = "api.example.com:8088"
    AUTH = basic_auth(USERNAME, PASSWORD)

    @pass_requests(BASEURL, AUTH, schema=SCHEMA)
    def get_data_example(req: RequestsAPI, value) -> list:
        # http://api.example.com:8088/api/v1/data?field_name=field_value
        return req.request("GET", "api/v1/data", query_params={"field_name": value})

    response = get_data_example("field_value")