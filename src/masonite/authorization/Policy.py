from .AuthorizationResponse import AuthorizationResponse


class Policy:
    def allow(cls, message="", code=None):
        return AuthorizationResponse.allow(True, code, message)

    def deny(cls, message="", code=None):
        return AuthorizationResponse.deny(False, code, message)
