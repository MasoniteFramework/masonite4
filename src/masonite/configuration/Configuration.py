import importlib
import inspect
import pkgutil
from os.path import relpath
from dotty_dict import dotty

from ..exceptions import InvalidConfigurationLocation


class Configuration:
    def __init__(self, application):
        self.application = application
        self._config = dotty()

    def load(self):
        """At boot load configuration from all files and store them in here."""
        config_root = self.application.make("config.location")

        for (module_loader, name, _) in pkgutil.iter_modules([config_root]):
            module_path = relpath(module_loader.path)
            obj_in_modules = importlib.import_module(
                module_path.replace("/", ".") + "." + name
            )
            for obj in inspect.getmembers(obj_in_modules):
                if obj[0].isupper():
                    self._config[f"{name}.{obj[0].lower()}"] = obj[1]
        # check loaded configuration
        if len(self._config.keys()) == 0 or "application" not in self._config:
            raise InvalidConfigurationLocation(
                f"Config directory {config_root} does not contain required configuration files."
            )

    def set(self, path, value):
        self._config[path] = value

    def get(self, path, default=None):
        try:
            return self._config[path]
        except KeyError:
            return default
