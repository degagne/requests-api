from requests.auth import HTTPBasicAuth
from requests.auth import HTTPDigestAuth
from requests_oauthlib import OAuth2
from requests_ntlm3 import HttpNtlmAuth
from requests_ntlm3 import NtlmCompatibility
from requests_kerberos import HTTPKerberosAuth, REQUIRED


def basic_auth(username: str, password: str) -> HTTPBasicAuth:
    """
    Creates a HTTP Basic Authentication object to provide the `Request` object.

    :param username: Username
    :param password: Password
    """
    return HTTPBasicAuth(username, password)


def digest_auth(username: str, password: str) -> HTTPDigestAuth:
    """
    Creates a HTTP Digest Authentication object to provide the `Request` object.

    :param username: Username
    :param password: Password
    """
    return HTTPDigestAuth(username, password)


def oauth2_auth(client_id: int, token: dict) -> OAuth2:
    """
    Creates an OAuth2 Authentication object to provide the `Request` object.

    :param client_id: Client ID obtained during registration
    :param token: Token dictionary, must include access_token and token_type
    """
    return OAuth2(client_id, None, token)


def ntlm_auth(
    username: str,
    password: str,
    send_cbt: bool = False,
    ntlm_compatibility: int = NtlmCompatibility.NTLMv2_DEFAULT
) -> HttpNtlmAuth:
    """
    Creates an NTLM Authentication object to provide the `Request` object.

    :param username: Username in 'domain\\username' format
    :param password: Password
    :param send_cbt: Send channel bindings over a HTTPS channel?
    :param ntlm_compatibility: Compatibility level for auth message
    """
    return HttpNtlmAuth(username, password, send_cbt, ntlm_compatibility)


def kerberos_auth(
    mutual_authentication: int = REQUIRED,
    service: str = "HTTP",
    delegate: bool = False,
    force_preemptive: bool = False,
    principal: str = None,
    hostname_override: str = None,
    sanitize_mutual_error_response: bool = True,
    send_cbt: bool = True
) -> HTTPKerberosAuth:
    """
    Creates a Kerberos Authentication object to provide the `Request` object.

    **REQUIRES** a valid Ticket-Granting-Ticket (TGT).

    :param mutual_authentication: Enable mutual authentication?
    :param service: Service type for header.
    :param delegate: Enable credential delegation?
    :param force_preemptive: Force Kerberos GSS exchange prior to 401 Unauthorized response
    :param principal: Override the default principal
    :param hostname_override: Override hostname
    """
    return HTTPKerberosAuth(
        mutual_authentication,
        service,
        delegate,
        force_preemptive,
        principal,
        hostname_override,
        sanitize_mutual_error_response,
        send_cbt
    )