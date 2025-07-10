from fastapi import HTTPException, status

class TokenDataException(HTTPException):
    def __init__(self, status_code: int | None = None, detail: str | None = None):
        self.status_code = status_code or status.HTTP_403_FORBIDDEN
        self.detail = detail or "Invalid token"
        super().__init__(self.status_code, self.detail)

class TokenAlreadyRevoked(HTTPException):
    def __init__(self, status_code: int | None = None, detail: str | None = None):
        self.status_code = status_code or status.HTTP_403_FORBIDDEN
        self.detail = detail or "Token revoked"
        super().__init__(self.status_code, self.detail)