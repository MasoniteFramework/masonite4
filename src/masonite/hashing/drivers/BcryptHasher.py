import bcrypt


class BcryptHasher:
    def __init__(self, options={}):
        self.options = options

    def set_options(self, options):
        self.options = options
        return self

    def make(self, string):
        rounds = self.options.get("rounds")
        salt = bcrypt.gensalt(rounds=rounds)
        return str(bcrypt.hashpw(bytes(string, "utf-8"), salt))
        # return str(bytes(bcrypt.hashpw(bytes(string, "utf-8"), bcrypt.gensalt())).decode("utf-8")

    def check(self, plain_string, hashed_string):
        rounds = self.options.get("rounds")
        # TODO: here we should take care of comparing use same rounds count
        # byt bcrypt does not expose public api to do this !
        # salt = bcrypt.gensalt(rounds=rounds)
        # ref_hashed = bcrypt.hashpw(bytes(plain_string, "utf-8"), salt)
        if not isinstance(hashed_string, bytes):
            hashed_string = bytes(hashed_string or "", "utf-8")
        return bcrypt.checkpw(bytes(plain_string, "utf-8"), hashed_string)
