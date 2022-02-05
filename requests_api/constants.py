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
