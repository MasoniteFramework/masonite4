from ...utils.helpers import random_string


class HasTokens:
    def generate_new_token(self):
        return random_string(60)
