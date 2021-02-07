class Session:
    def __init__(self, application, driver_config=None):
        self.application = application
        self.drivers = {}
        self._driver = None
        self.driver_config = driver_config or {}
        self.options = {}

    def add_driver(self, name, driver):
        self.drivers.update({name: driver})

    def driver(self, driver):
        return self.drivers[driver]

    def set_configuration(self, config):
        self.driver_config = config
        return self

    def get_driver(self, name=None):
        if name is None:
            return self.drivers[self.driver_config.get("default")]
        return self.drivers[name]

    def get_config_options(self, driver=None):
        if driver is None:
            return self.driver_config[self.driver_config.get("default")]

        return self.driver_config.get(driver, {})
