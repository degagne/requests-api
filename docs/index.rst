============
Requests-API
============

.. toctree::
    :titlesonly:
    :hidden:

    api.rst

The ``Requests-API`` is a library I created to ease the use of the ``requests`` library for my internal projects.
So I figured why not share it in case it helps someone out.

Installation
============

Before installation, please make sure you have at least Python 3.6 installed on our system.

.. code-block:: bash
    :caption: Bash

    $ pip install requests-api

Usage
=====

Create a ``Retries`` object for the automatic retry mechanism.

.. code-block:: python
    :caption: Python

    from requests_api.retries import Retries

    configs = {"status": 5, "read": 1, "status_forcelist": [500]}
    retries = Retries(**configs)

For additional information on ``Retries``, see `urllib3 <https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html>`_

Create an authentication object. Supports

- HTTPBasicAuth - `requests <https://docs.python-requests.org/en/latest/api/#authentication>`_
- HTTPDigestAuth - `requests <https://docs.python-requests.org/en/latest/api/#authentication>`_
- OAuth2 - `requests_oauthlib <https://requests-oauthlib.readthedocs.io/en/latest/oauth2_workflow.html>`_
- HttpNtlmAuth - `requests_ntlm3 <https://pypi.org/project/requests-ntlm3/>`_
- HTTPKerberosAuth - `requests_kerberos <https://pypi.org/project/requests-kerberos/>`_

.. code-block:: python
    :caption: Python

    from requests_api import basic_auth

    auth = basic_auth("username", "supersecurepassword")

Create ``RequestsAPI`` object.

.. code-block:: python
    :caption: Python

    from requests_api import RequestsAPI

    baseurl = "whatever.example.com"

    r = RequestsAPI(baseurl, auth, retries=retries)
    response = r.request("GET", "some/api/path/here", query_params={"fields": "something"})

The ``RequestsAPI`` also has a decorator object which can simplify the process and search for keys within the response object.

.. code-block:: python
    :caption: Python

    from requests_api import request_decorator

    @request_decorator(["guid", "service", "name"])
    def get_policy_id(policy_id) -> list:
        r = RequestsAPI(BASEURL, AUTH, retries=RETRIES)
        return r.request("GET", f"service/public/v2/api/policy/{policy_id}")

    response = get_policy_id(3)

    License
    =======
    
    ``requests-api`` is licensed under MIT license. See the `LICENSE <https://github.com/degagne/requests-api/blob/master/LICENSE>`_ for more information
    
    Links
    =====

    - `Python Site <https://www.python.org/>`_
    - `PyPI Site <https://pypi.org/>`_
    - `urllib3 <https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html>`_
    - `requests <https://docs.python-requests.org/en/latest/>'_
    - `requests_oauthlib <https://pypi.org/project/requests-oauthlib/>`_
    - `requests_ntlm3 <https://pypi.org/project/requests-ntlm3/>`_
    - `requests_kerberos <https://pypi.org/project/requests-kerberos/>`_