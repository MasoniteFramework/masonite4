class Auth:
    def __init__(self, application, guard_config=None):
        self.application = application
        self.guards = {}
        self._guard = None
        self.guard_config = guard_config or {}
        self.options = {}

    def add_guard(self, name, guard):
        self.guards.update({name: guard})

    def set_configuration(self, config):
        self.guard_config = config
        return self

    def guard(self, guard):
        self._guard = guard
        return self

    def get_guard(self, name=None):
        if name is None and self._guard is None:
            return self.guards[self.guard_config.get("default")]

        return self.guards[self._guard]

    def get_config_options(self, guard=None):
        if guard is None:
            options = self.guard_config.get(self.guard_config.get("default"), {})
            options.update(self.options)
            return options

        options = self.guard_config.get(guard, {})
        options.update(self.options)
        return options

    def attempt(self, email, password, once=False):
        auth_config = self.get_config_options()
        auth_config.update({'once': once})
        return self.get_guard().set_options(auth_config).attempt(email, password)  

    def attempt_by_id(self, user_id, once=False):
        auth_config = self.get_config_options()
        auth_config.update({'once': once})
        return self.get_guard().set_options(auth_config).attempt_by_id(user_id)  
    
    def logout(self):
        """Logout the current authenticated user.

        Returns:
            self
        """
        self.application.make("request").remove_user()
        return self.application.make("request").delete_cookie("token")
    
    def user(self):
        """Logout the current authenticated user.

        Returns:
            self
        """
        auth_config = self.get_config_options()
        return self.get_guard().set_options(auth_config).user()  
        