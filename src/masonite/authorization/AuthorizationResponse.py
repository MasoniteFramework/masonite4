from ..exceptions.exceptions import AuthorizationException


class AuthorizationResponse:
    def __init__(self, allowed, code=None, message=""):
        self._allowed = allowed
        self.code = code
        self.message = message

    def get_response(self):
        return ""

    @classmethod
    def allow(cls, code=None, message=""):
        return cls(True, code, message)

    @classmethod
    def deny(cls, code=None, message=""):
        return cls(False, code, message)

    def allowed(self):
        return self._allowed

    def authorize(self):
        if not self._allowed:
            raise AuthorizationException(self.code, self.message)
        return self

    def get_response(self):
        return self.message, self.code

    def message(self):
        return self.message
