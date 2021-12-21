import jwt


class AuthenticatesTokens:

    __TOKEN_COLUMN__ = "api_token"

    def generate_jwt(self):
        token = jwt.encode({"email": self.email}, "secret", algorithm="HS512")
        setattr(self, self.__TOKEN_COLUMN__, token)
        self.save()
        return token
