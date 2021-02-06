"""Authentication Class."""


class Auth:
    def __init__(self, application):
        self.application = application
        self.guards = {}
        self.model = None

    def guard(self, name):
        return self.guards[name].set_authentication_model(self.model)

    def set_guard(self, name, guard):
        self.guards.update({name: guard})

    def set_authentication_model(self, model):
        self.model = model
        return self
