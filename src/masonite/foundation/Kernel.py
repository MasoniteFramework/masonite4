class Kernel:
    def __init__(self, app):
        self.application = app

    def register(self):
        self.register_controllers()
        self.register_templates()

    def register_controllers(self):
        self.application.bind(
            "controller.location", 
            "tests.integrations.controllers"
        )

    def register_templates(self):
        self.application.bind(
            "views.location",
            "tests/integrations/templates"
        )
