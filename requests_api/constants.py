# supported method types
GET    = "GET"
HEAD   = "HEAD"
POST   = "POST"
PUT    = "PUT"
DELETE = "DELETE"
PATCH  = "PATCH"

# expected http status codes per method type
STATUS_CODES = {
    GET:    [200],
    HEAD:   [200],
    POST:   [200, 201, 204],
    PUT:    [200, 202, 204],
    DELETE: [200, 202, 204],
    PATCH:  [200, 204]
}

# retry backoff factor
BACKOFF_FACTOR   = 2

# retry forcelist of http status codes
STATUS_FORCELIST = [500, 502, 503]

# retry allowed methods
ALLOWED_METHODS  = frozenset([GET, HEAD, POST, PUT, DELETE, PATCH])

# default headers for all requests
HEADERS = {"Content-type": "application/json"}

# default maximum number of retries
MAX_RETRIES = 5

# default schema for requests
SCHEMA = "https"