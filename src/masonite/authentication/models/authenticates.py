"""Password Helper Module."""
import bcrypt
import uuid


class Authenticates:

    __auth__ = "email"
    __password__ = "password"

    def attempt(self, username, password):
        """Attempts to login using a username and password"""
        record = self.where(self.get_username_column(), username).first()
        if not record:
            return False

        record_password = getattr(record, self.get_password_column())
        if not isinstance(record_password, bytes):
            record_password = bytes(record_password or "", "utf-8")
        if self.verify_password(password, record_password):
            record.set_remember_token().save()
            return record

        return False

    def verify_password(self, password, record_password):
        if hasher == "bcrypt":
            return bcrypt.checkpw(bytes(password, "utf-8"), record_password)
        elif hasher == "argon2":
            from argon2 import PasswordHasher

            ph = PasswordHasher()
            return ph.verify(record_password, password)
        else:
            raise Exception("No password_hasher defined !")

    def hash_password(self, password):
        if hasher == "bcrypt":
            from ...utils.helpers import password as bcrypt_password

            return str(bcrypt_password(password))
        elif hasher == "argon2":
            from argon2 import PasswordHasher

            ph = PasswordHasher()
            return str(ph.hash(password))
        else:
            raise Exception("No password_hasher defined !")

    def register(self, dictionary):
        dictionary.update(
            {
                self.get_password_column(): self.hash_password(
                    dictionary.get("password", "")
                )
            }
        )
        return self.create(dictionary)

    def get_id(self):
        return self.get_primary_key_value()

    def attempt_by_id(self, user_id):
        """Attempts to login using a username and password"""
        record = self.find(user_id)
        if not record:
            return False

        record.set_remember_token().save()
        return record

    def get_remember_token(self):
        """Attempts to login using a username and password"""
        return self.remember_token

    def set_remember_token(self, token=None):
        """Attempts to login using a username and password"""
        self.remember_token = str(token) if token else str(uuid.uuid4())
        return self

    def reset_password(self, username, password):
        """Attempts to login using a username and password"""
        self.where(self.get_username_column(), username).update(
            {self.get_password_column(): self.hash_password(password)}
        )
        return self

    def get_password_column(self):
        """Attempts to login using a username and password"""
        return self.__password__

    def get_username_column(self):
        """Attempts to login using a username and password"""
        return self.__auth__
