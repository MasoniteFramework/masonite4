from argon2 import PasswordHasher


class Argon2Hasher:
    def __init__(self, options={}):
        self.options = options

    def set_options(self, options):
        self.options = options
        return self

    def make(self, string):
        ph = PasswordHasher()
        return str(ph.hash(bytes(string, "utf-8")))

    def check(self, plain_string, hashed_string):
        ph = PasswordHasher()
        return ph.verify(hashed_string, bytes(plain_string, "utf-8"))
