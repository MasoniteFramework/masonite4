from .AuthorizationResponse import AuthorizationResponse


class Gate:
    def __init__(self, application, user_callback=None):
        self.application = application
        self.user_callback = user_callback

        self.policies = []
        self.permissions = {}
        self.before_callbacks = []
        self.after_callbacks = []

    def define(self, permission, condition):
        if not callable(condition):
            raise Exception(f"Permission {permission} should be given a callable.")

        self.permissions.update({permission: condition})

    def before(self, before_callback):
        if not callable(before_callback):
            raise Exception(f"before() should be given a callable.")
        self.before_callbacks.append(before_callback)

    def after(self, after_callback):
        if not callable(after_callback):
            raise Exception(f"before() should be given a callable.")
        self.after_callbacks.append(after_callback)

    def allows(self, permission, *args):
        return self.inspect(permission, *args).allowed()

    def denies(self, permission, *args):
        return not self.inspect(permission, *args).allowed()

    def has(self, permission):
        return permission in self.permissions

    def for_user(self, user):
        return Gate(self.application, lambda: user)

    def any(self, permissions, *args):
        # TODO:
        pass

    def none(self, permissions, *args):
        # TODO:
        pass

    def authorize(self, permission, *args):
        return self.inspect(permission, *args).authorize()

    def inspect(self, permission, *args):
        """Get permission checks results for the given user then builds and returns an
        authorization response."""
        boolean_result = self.check(permission, *args)
        if isinstance(boolean_result, AuthorizationResponse):
            return boolean_result
        if boolean_result:
            return AuthorizationResponse.allow()
        else:
            return AuthorizationResponse.deny()

    def check(self, permission, *args):
        """The core of the authorization class. Run before() checks, permission check and then
        after() checks."""
        user = self._get_user()

        # run before checks and returns immediately if non null response
        result = None
        for callback in self.before_callbacks:
            result = callback(user, permission)
            if result:
                break

        # run permission checks if nothing returned previously
        if result is None:
            result = self.permissions[permission](user, *args)

        # run after checks
        for callback in self.after_callbacks:
            after_result = callback(user, permission, result)
            result = after_result if after_result is not None else result

        return result

    def _get_user(self):
        from ..facades import Request

        if self.user_callback:
            return self.user_callback()
        else:
            return Request.user()
