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

    def get(self, key, default=None):
        """Get a value from the session.

        Arguments:
            key {string} -- The key to get from the session.
            default|None -- The default value to return if value does not exist

        Returns:
            string|default - Returns default if a value does not exist.
        """
        response = self.get_response()
        cookie = response.cookie("s_{0}".format(key))
        if cookie:
            return self._get_serialization_value(cookie)

        cookie = response.cookie("f_{0}".format(key))
        if cookie:
            return self._get_serialization_value(cookie)

        return default

    def pull(self, key, default=None):
        """Get a value from the session and then forget it.

        Arguments:
            key {string} -- The key to get from the session.
            default|None -- The default value to return if value does not exist
        """
        value = self.get(key, default)
        self.delete(key)
        return value

    def _get_serialization_value(self, value):
        try:
            if isinstance(value, str):
                value = value.replace("'", '"')
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

    def push(self, key, value):
        """Push a value in the session on a key which is an array

        Arguments:
            key {string} -- The key to set as the session key.
            value {string} -- The value to set in the session.
        """
        array = self.get(key, [])
        array.append(value)
        self.set(key, array)

    def increment(self, key, amount=1):
        self.set(key, self.get(key, 0) + amount)

    def decrement(self, key, amount=-1):
        self.increment(key, amount)

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
        # @check: not sure this one is needed
        # self.__collect_data()

        response = self.get_response()

        if response.cookie("s_{}".format(key)):
            response.delete_cookie("s_{}".format(key))
            return True

        return False

    def flush(self):
        """Delete all session data"""
        response = self.get_response()
        all_cookies = response.cookie_jar.to_dict()
        for key, value in all_cookies.items():
            if not (key.startswith("f_") or key.startswith("s_")):
                continue
            response.delete_cookie(key)

    def start(self, request):
        response = self.get_response()
        for key, value in request.cookie_jar.to_dict().items():
            if not (key.startswith("f_") or key.startswith("s_")) or key.startswith(
                "_flash."
            ):
                continue
            response.cookie_jar.load_cookie(key, self._get_serialization_value(value))

    def save(self):
        self.age_flash_data()

    def age_flash_data(self):
        """Age flash data for the session."""
        for key in list(self.get("_flash.old", [])):
            self.delete(key)
        self.set("_flash.old", self.get("_flash.new", []))
        self.set("_flash.new", [])

    def get_response(self):
        return self.application.make("response")

    def get_request(self):
        return self.application.make("request")

    def __collect_data(self, flash_only=False):
        """Collect data from session and flash data.

        Returns:
            dict
        """
        cookies = {}
        request = self.get_request()
        all_cookies = request.cookie_jar.to_dict()
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
        self.set(key, value)
        self.push("_flash.new", key)
        # if isinstance(value, (dict, list)):
        #     value = json.dumps(value)

        # response = self.get_response()
        # response.cookie(
        #     "f_{0}".format(key),
        #     str(value),
        # )
        self.set("_flash.old", list(set(self.get("_flash.old", [])) - set([key])))

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
