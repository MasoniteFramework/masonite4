import uuid

from ...utils.helpers import password


class WebGuard:
    def __init__(self, application):
        self.application = application
        self._once = False
        self.model = None

    def set_authentication_model(self, model):
        self.model = model
        return self

    def user(self):
        """Get the currently logged in user.

        Raises:
            exception -- Raised when there has been an error handling the user model.

        Returns:
            object|bool -- Returns the current authenticated user object or False or None if there is none.
        """
        token = self.application.make("request").cookie("token")
        if token and self.model:
            return self.model.where("remember_token", token).first() or False

        return False

    def attempt(self, username, password):
        """Login the user based on the parameters provided.

        Arguments:
            name {string} -- The field to authenticate. This could be a username or email address.
            password {string} -- The password to authenticate with.

        Raises:
            exception -- Raised when there has been an error handling the user model.

        Returns:
            object|bool -- Returns the current authenticated user object or False or None if there is none.
        """

        attempt = self.model.attempt(username, password)
        if attempt:
            self.application.make("request").cookie("token", attempt.remember_token)
            return attempt

        return False

    def logout(self):
        """Logout the current authenticated user.

        Returns:
            self
        """
        self.application.make("request").remove_user()
        return self.application.make("request").delete_cookie("token")

    def login_by_id(self, user_id):
        """Login a user by the user ID.

        Arguments:
            user_id {string|int} -- The ID of the user model record.

        Returns:
            object|False -- Returns the current authenticated user object or False or None if there is none.
        """
        model = self.model.find(user_id)

        if model:
            if not self._once:
                remember_token = str(uuid.uuid4())
                model.remember_token = remember_token
                model.save()
                self.driver.save(remember_token, model=model)
            self.app.make("request").set_user(model)
            return model

        return False

    def once(self):
        """Log in the user without saving a cookie.

        Returns:
            self
        """
        self._once = True
        return self

    def _get_password_column(self, model):
        """Gets the password column to use.

        Arguments:
            model {orator.orm.Model} -- An Orator type model.

        Returns:
            string
        """
        if hasattr(model, "__password__"):
            return getattr(model, model.__password__)

        if hasattr(model, "password"):
            return getattr(model, "password")

    def register(self, user):
        """Register the user.

        Arguments:
            user {dict} -- A dictionary of user data information.
        """
        user["password"] = password(user["password"])
        return self.model.create(**user)
