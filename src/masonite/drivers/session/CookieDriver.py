"""Session Cookie Module."""

import json
from email import message


class CookieDriver:
    """Cookie Session Driver."""

    def __init__(self, application):
        """Cookie Session Constructor.

        Arguments:
            application {dict} -- The application class
        """
        self.application = application

    def get(self, key):
        """Get a value from the session.

        Arguments:
            key {string} -- The key to get from the session.

        Returns:
            string|None - Returns None if a value does not exist.
        """
        response = self.get_response()
        cookie = response.cookie("s_{0}".format(key))
        if cookie:
            return self._get_serialization_value(cookie)

        cookie = response.cookie("f_{0}".format(key))
        if cookie:
            return self._get_serialization_value(cookie)

        return None

    def _get_serialization_value(self, value):
        try:
            return json.loads(value)
        except (ValueError, TypeError):
            return value

    def set(self, key, value):
        """Set a value in the session.

        Arguments:
            key {string} -- The key to set as the session key.
            value {string} -- The value to set in the session.
        """
        if isinstance(value, dict):
            value = json.dumps(value)

        response = self.get_response()

        response.cookie("s_{0}".format(key), str(value))

    def has(self, key):
        """Check if a key exists in the session.

        Arguments:
            key {string} -- The key to check for in the session.

        Returns:
            bool
        """
        if self.get(key):
            return True
        return False

    def all(self, flash_only=False):
        """Get all session data.

        Returns:
            dict
        """
        return self.__collect_data(flash_only=flash_only)

    def delete(self, key):
        """Delete a value in the session by it's key.

        Arguments:
            key {string} -- The key to find in the session.

        Returns:
            bool -- If the key was deleted or not
        """
        self.__collect_data()

        response = self.get_response()

        if response.cookie("s_{}".format(key)):
            response.delete_cookie("s_{}".format(key))
            return True

        return False

    def get_response(self):
        return self.application.make("response")

    def __collect_data(self, flash_only=False):
        """Collect data from session and flash data.

        Returns:
            dict
        """
        cookies = {}
        response = self.get_response()
        all_cookies = response.cookie_jar.to_dict()
        for key, value in all_cookies.items():
            if not (key.startswith("f_") or key.startswith("s_")):
                continue

            if flash_only and not key.startswith("f_"):
                continue

            key = key.replace("f_", "").replace("s_", "")

            cookies.update({key: self.get(key)})
        return cookies

    def flash(self, key, value):
        """Add temporary data to the session.

        Arguments:
            key {string} -- The key to set as the session key.
            value {string} -- The value to set in the session.
        """
        if isinstance(value, (dict, list)):
            value = json.dumps(value)

        response = self.get_response()
        response.cookie(
            "f_{0}".format(key),
            str(value),
        )

    def get_error_messages(self):
        """Should get and delete the flashed messages

        Arguments:
            key {string} -- The key to set as the session key.
            value {string} -- The value to set in the session.
        """
        only_messages = []
        messages = self.all(flash_only=True).get("errors", {}).items()
        for key, messages in messages:
            for error_message in messages:
                only_messages.append(error_message)
        self.reset(flash_only=True)
        return only_messages

    def get_flashed_messages(self):
        """Should get and delete the flashed messages

        Arguments:
            key {string} -- The key to set as the session key.
            value {string} -- The value to set in the session.
        """
        messages = self.all(flash_only=True)
        self.reset(flash_only=True)
        return messages

    def reset(self, flash_only=False):
        """Delete all session data.

        Keyword Arguments:
            flash_only {bool} -- If only flash data should be deleted. (default: {False})
        """
        cookies = self.__collect_data()
        response = self.get_response()
        for cookie in cookies:
            if flash_only:
                response.delete_cookie("f_{0}".format(cookie))
                continue

            response.delete_cookie("s_{0}".format(cookie))

    def helper(self):
        """Use to create builtin helper function."""
        return self
