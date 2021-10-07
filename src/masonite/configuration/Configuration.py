import inspect
import pkgutil
import pydoc
from os.path import relpath
from dotty_dict import dotty

from ..exceptions import InvalidConfigurationLocation, InvalidConfigurationSetup


# from PR #147 not merged yet, in the meantime hard-coded here
# from ..utils.structures import load
# from ..utils.str import modularize


def modularize(path):
    return path.replace("/", ".").rstrip(".py")


def load(path, object_name=None, default=None):
    """Load the given object from a Python module located at path and returns a default
    value if not found. If no object name is provided, loads the module.

    Arguments:
        path {str} -- A file path or a dotted path of a Python module
        object {str} -- The object name to load in this module (None)
        default {str} -- The default value to return if object not found in module (None)
    Returns:
        {object} -- The value (or default) read in the module or the module if no object name
    """
    # modularize path if needed
    dotted_path = modularize(path)
    module = pydoc.locate(dotted_path)
    if object_name is None:
        return module
    else:
        return getattr(module, object_name, default)


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
        self._config = dotty()

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
        (such as 'application'.)
        """
        if path in self.reserved_keys:
            raise InvalidConfigurationSetup(
                f"{path} is a reserved configuration key name. Please use an other key."
            )
        if isinstance(external_config, str):
            # config is a path and should be loaded
            module = load(external_config)
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
