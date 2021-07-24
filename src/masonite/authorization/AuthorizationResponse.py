from ..exceptions.exceptions import AuthorizationException


class AuthorizationResponse:
    def __init__(self, allowed, message="", code=None):
        self._allowed = allowed
        self.code = code
        self._message = message

    @classmethod
    def allow(cls, message="", code=None):
        return cls(True, message, code)

    @classmethod
    def deny(cls, message="", code=None):
        return cls(False, message, code)

    def allowed(self):
        return self._allowed

    def authorize(self):
        if not self._allowed:
            raise AuthorizationException(self.code, self._message)
        return self

    def get_response(self):
        return self._message, self.code

    def message(self):
        return self._message
