class Session:
    def __init__(self, application, driver_config=None):
        self.application = application
        self.drivers = {}
        self._driver = None
        self.driver_config = driver_config or {}
        self.options = {}
        self.data = {}
        self.added = {}
        self.deleted = []

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

    # Start of methods
    def start(self, driver=None):
        self.data = {}
        self.added = {}
        self.deleted = []
        self.data = self.get_driver(name=driver).start()
        return self

    def get_data(self):
        data = self.data
        data.update(self.added)
        for deleted in self.deleted:
            data.pop(deleted)
        return data

    def save(self, driver=None):
        return self.get_driver(name=driver).save(added=self.added, deleted=self.deleted)

    def set(self, key, value):
        return self.added.update({key: value})

    def get(self, key):
        return self.get_data().get(key)

    def pull(self, key):
        key_value = self.get(key)
        self.delete(key)
        return key_value

    def delete(self, key):
        return self.deleted.append(key)

    def flash(self, key, value, driver=None):
        """Add temporary data to the session.

        Arguments:
            key {string} -- The key to set as the session key.
            value {string} -- The value to set in the session.
        """
        return self.get_driver(name=driver).flash(key, value)

    def reset(self, driver=None, flash_only=False):
        """Delete all session data.

        Keyword Arguments:
            flash_only {bool} -- If only flash data should be deleted. (default: {False})
        """
        return self.get_driver(name=driver).reset(flash_only=flash_only)

    def has(self, key, driver=None):
        """Check if a key exists in the session.

        Arguments:
            key {string} -- The key to check for in the session.

        Returns:
            bool
        """
        return self.get_driver(name=driver).has(key)

    def all(self, flash_only=False, driver=None):
        """Get all session data.

        Returns:
            dict
        """
        return self.get_driver(name=driver).all(flash_only=flash_only)

    def get_flashed_messages(self, driver=None):
        """Get flashed messages session data.

        Returns:
            dict
        """
        return self.get_driver(name=driver).get_flashed_messages()
