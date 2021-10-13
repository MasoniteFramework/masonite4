import inspect
import pkgutil
from os.path import relpath

from ..utils.structures import data, load
from ..exceptions import InvalidConfigurationLocation, InvalidConfigurationSetup


class Configuration:
    # Foundation configuration keys
    reserved_keys = [
        "application",
        "auth",
        "broadcast",
        "cache",
        "database",
        "filesystem",
        "mail",
        "notification",
        "providers",
        "queue",
        "session",
    ]

    def __init__(self, application):
        self.application = application
        self._config = data()

    def load(self):
        """At boot load configuration from all files and store them in here."""
        config_root = self.application.make("config.location")
        for module_loader, name, _ in pkgutil.iter_modules([config_root]):
            module = load(f"{relpath(module_loader.path)}.{name}")
            params = self._get_params_from_module(module)
            for param in params:
                self._config[f"{name}.{param[0].lower()}"] = param[1]

        # check loaded configuration
        if not self._config.get("application"):
            raise InvalidConfigurationLocation(
                f"Config directory {config_root} does not contain required configuration files."
            )

    def merge_with(self, path, external_config):
        """Merge external config at key with project config at same key. It's especially
        useful in Masonite packages in order to merge the configuration default package with
        the package configuration which can be published in project.

        This functions disallow merging configuration using foundation configuration keys
        (such as 'application').
        """
        if path in self.reserved_keys:
            raise InvalidConfigurationSetup(
                f"{path} is a reserved configuration key name. Please use an other key."
            )
        if isinstance(external_config, str):
            # config is a path and should be loaded
            module = load(relpath(external_config))
            params = self._get_params_from_module(module)
            base_config = {name.lower(): value for name, value in params}
        else:
            base_config = {
                name.lower(): value for name, value in external_config.items()
            }
        merged_config = {**base_config, **self.get(path, {})}
        self.set(path, merged_config)

    def set(self, path, value):
        self._config[path] = value

    def get(self, path, default=None):
        try:
            return self._config[path]
        except KeyError:
            return default

    def _get_params_from_module(self, module):
        params = []
        for obj in inspect.getmembers(module):
            obj_name = obj[0]
            if (
                obj_name.isupper()
                and not obj_name.startswith("__")
                and not obj_name.endswith("__")
            ):
                params.append(obj)
        return params
