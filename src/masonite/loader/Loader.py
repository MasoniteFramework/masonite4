"""Loader class to easily list, find or load any object in a given module, or folder."""
import inspect
import pkgutil
import os

from ..exceptions import LoaderNotFound
from ..utils.str import filepath
from ..utils.structures import load

"""
API:
# all paths can be

## for folders
tests/integrations/app
tests.integrations.app

## for files
tests/integrations/app/User
tests/integrations/app/User.py
tests.integrations.app.User
tests.integrations.app.User.py

# if start with / => look for absolute, else start from project root.

# recursive search of a class in a list of directories or files
list_of_classes = loader.list_classes(class, paths)
list_of_classes = loader.list_classes(Model, ["tests/integrations/app", "project/app"])

# load a class from a file
list_of_classes = loader.get_class(class, path)
list_of_classes = loader.get_class(class, "tests/integrations/app/User")

# load objects from a module
list_of_objects = loader.get_objects(path, filter)
list_of_objects = loader.get_objects(
    path,
    lambda obj: obj_name.isupper() and not obj_name.startswith("__") and not obj_name.endswith("__")
)

# find a given object in a given module or in given modules (the first one find)
loader.find(Model, [..., ...])
loader.find(Model, [..., ...], "User")
OR
loader.find(Model, one_module)
loader.find(Model, one_module, "User")

"""


def parameters_filter(obj_name, obj):
    return (
        obj_name.isupper()
        and not obj_name.startswith("__")
        and not obj_name.endswith("__")
    )


class Loader:
    def get_modules(self, files_or_directories):
        if not isinstance(files_or_directories, list):
            files_or_directories = [files_or_directories]

        _modules = {}
        module_paths = list(map(filepath, files_or_directories))
        for module_loader, name, _ in pkgutil.iter_modules(module_paths):
            module = load(f"{os.path.relpath(module_loader.path)}.{name}")
            _modules.update({name: module})
        return _modules

    def find(self, class_instance, paths, class_name, raise_exception=False):
        _classes = self.find_all(class_instance, paths)
        for name, obj in _classes.items():
            if name == class_name:
                return obj
        if raise_exception:
            raise LoaderNotFound(
                f"No {class_instance} named {class_name} has been found in {paths}"
            )
        return None

    def find_all(self, class_instance, paths, raise_exception=False):
        _classes = {}
        for module in self.get_modules(paths).values():
            for obj_name, obj in inspect.getmembers(module):
                # check if obj is the same class as the given one
                if inspect.isclass(obj) and issubclass(obj, class_instance):
                    # check if the class really belongs to those paths to load internal only
                    if obj.__module__.startswith(module.__package__):
                        _classes.update({obj_name: obj})
        if not len(_classes.keys()) and raise_exception:
            raise LoaderNotFound(f"No {class_instance} have been found in {paths}")
        return _classes

    def get_objects(self, path_or_module, filter_method=None):
        """Returns a dictionary of objects from the given path (file or dotted). The dictionary can
        be filtered if a given callable is given."""
        if isinstance(path_or_module, str):
            module = load(path_or_module)
        else:
            module = path_or_module
        if not module:
            return None
        return dict(inspect.getmembers(module, filter_method))

    def get_parameters(self, module_or_path):
        _parameters = {}
        for name, obj in self.get_objects(module_or_path).items():
            if parameters_filter(name, obj):
                _parameters.update({name: obj})

        return _parameters
