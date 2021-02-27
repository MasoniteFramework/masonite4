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
        if bcrypt.checkpw(bytes(password, "utf-8"), record_password):
            record.set_remember_token().save()
            return record

        return False

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

    def get_password_column(self):
        """Attempts to login using a username and password"""
        return self.__password__

    def get_username_column(self):
        """Attempts to login using a username and password"""
        return self.__auth__
