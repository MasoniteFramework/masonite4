class Mail:
    def __init__(self, application, driver_config=None):
        self.application = application
        self.drivers = {}
        self._driver = "smtp"
        self.driver_config = driver_config or {}
        self.options = {}

    def add_driver(self, name, driver):
        self.drivers.update({name: driver})

    def set_configuration(self, config):
        self.driver_config = config
        return self

    def driver(self, name):
        self._driver = name
        return self

    def get_driver(self, name):
        return self.drivers[name]

    def get_config_options(self):
        return self.driver_config.get(self._driver, {})

    def mailable(self, mailable):
        options = mailable.set_application(self.application).build().get_options()
        options.update(self.get_config_options())
        self.options = options
        return self

    def send(self):
        return self.get_driver(self._driver).set_options(self.options).send()
