from enum import Enum


class RequestStatus(Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


class ErrorCode(Enum):
    NONE = "NONE"
    TIMEOUT = "TIMEOUT"
    MODEL_ERROR = "MODEL_ERROR"
    RETRIEVAL_ERROR = "RETRIEVAL_ERROR"
    RATE_LIMITED = "RATE_LIMITED"
