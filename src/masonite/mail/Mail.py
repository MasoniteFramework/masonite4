class Mail:
    def __init__(self, application, driver_config=None):
        self.application = application
        self.drivers = {}
        self.driver_config = driver_config or {}

    def add_driver(self, name, driver):
        self.drivers.update({name: driver})

    def set_configuration(self, config):
        self.driver_config = config
        return self

    def driver(self, name):
        return self.drivers[name]

    def get_config_options(self):
        return self.driver_config.get("smtp", {})

    def mailable(self, mailable):
        options = mailable.build().get_options()
        options.update(self.get_config_options())
        return self.driver("smtp").set_options(options).send()
