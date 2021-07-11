class Session:
    def __init__(self, application, driver_config=None):
        self.application = application
        self.drivers = {}
        self._driver = None
        self.driver_config = driver_config or {}
        self.options = {}
        self.data = {}
        self.added = {}
        self.flashed = {}
        self.deleted = []
        self.deleted_flashed = []

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
        self.flashed = {}
        self.deleted = []
        self.deleted_flashed = []
        started_data = self.get_driver(name=driver).start()
        self.data = started_data.get("data")
        self.flashed = started_data.get("flashed")
        return self

    def get_data(self):
        data = self.data
        data.update(self.added)
        data.update(self.flashed)
        for deleted in self.deleted:
            if deleted in data:
                data.pop(deleted)
        for deleted in self.deleted_flashed:
            if deleted in data:
                data.pop(deleted)
        return data

    def save(self, driver=None):
        return self.get_driver(name=driver).save(
            added=self.added,
            deleted=self.deleted,
            flashed=self.flashed,
            deleted_flashed=self.deleted_flashed,
        )

    def set(self, key, value):
        return self.added.update({key: value})

    def has(self, key):
        return key in self.get_data()

    def get(self, key):
        if key in self.flashed:
            value = self.flashed.get(key)
            self.flashed.pop(key)
            self.deleted_flashed.append(key)
            return value

        return self.get_data().get(key)

    def pull(self, key):
        key_value = self.get(key)
        self.delete(key)
        return key_value

    def flush(self):
        self.deleted += list(self.get_data().keys())

    def delete(self, key):
        self.deleted.append(key)
        if key in self.flashed:
            self.flashed.pop(key)

    def flash(self, key, value):
        """Add temporary data to the session.

        Arguments:
            key {string} -- The key to set as the session key.
            value {string} -- The value to set in the session.
        """
        self.flashed.update({key: value})

    def reset(self, driver=None, flash_only=False):
        """Delete all session data.

        Keyword Arguments:
            flash_only {bool} -- If only flash data should be deleted. (default: {False})
        """
        return self.get_driver(name=driver).reset(flash_only=flash_only)

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
