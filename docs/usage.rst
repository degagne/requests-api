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

Create ``Requests`` object
=============================

.. code-block:: python
    :caption: Python
    :linenos:
    
    from requests_api import Requests

    r = Requests("whatever.example.com", auth, retries=retries)
    response = r.request("GET", "some/api/path/here", query_params={"fields": "something"})

User's can also restrict the keys provided in the response with the following:

.. code-block:: python
    :caption: Python
    :linenos:
    
    from requests_api import Requests

    r = Requests("whatever.example.com", auth, retries=retries)
    response = r.request("GET", "some/api/path/here", query_params={"fields": "something"}, search_keys=["name1", "name2"])
