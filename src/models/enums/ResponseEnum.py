from enum import Enum
class ResponseSignal(Enum):
    SUCCESS = "success"
    ERROR = "error"
    NOT_FOUND = "not_found"
    UNAUTHORIZED = "unauthorized"
    FORBIDDEN = "forbidden"
    BAD_REQUEST = "bad_request"
    INTERNAL_SERVER_ERROR = "internal_server_error"
    CONFLICT = "conflict"
    CREATED = "created"
    ACCEPTED = "accepted"
    NO_CONTENT = "no_content"