"""Starts Interactive Console Command."""
import code
import sys
import pkgutil
import importlib
import inspect
import os
from cleo import Command

from ..utils.collections import Collection
from ..utils.structures import load

BANNER = """Masonite Python {} Console
This interactive console has the following things imported:
    container as 'app',
    {},
    {}

Type `exit()` to exit."""


class TinkerCommand(Command):
    """
    Run a python shell with the container pre-loaded.

    tinker
        {--i|ipython : Run a IPython shell}
    """

    def autoload_models(self, directories=[]):
        from masoniteorm.models import Model

        instance = Model
        classes = {}
        for (module_loader, name, _) in pkgutil.iter_modules(directories):
            search_path = module_loader.path
            for obj in inspect.getmembers(
                self._get_module_members(module_loader, name)
            ):
                if inspect.isclass(obj[1]) and issubclass(obj[1], instance):
                    if obj[1].__module__.startswith(search_path.replace("/", ".")):
                        classes.update({obj[1].__name__: obj[1]})
        return classes

    def _get_module_members(self, module_loader, name):
        search_path = module_loader.path
        if search_path.endswith("/"):
            raise Exception("Autoload path cannot have a trailing slash")

        return importlib.import_module(
            module_loader.path.replace("/", ".") + "." + name
        )

    def handle(self):
        from wsgi import application

        version = "{}.{}.{}".format(
            sys.version_info.major, sys.version_info.minor, sys.version_info.micro
        )
        models = self.autoload_models(["tests/integrations/app"])
        banner = BANNER.format(version, "Collection, load", ",".join(models.keys()))
        context = {"app": application, "Collection": Collection, "load": load, **models}

        if self.option("ipython"):
            try:
                import IPython
            except ImportError:
                raise ModuleNotFoundError(
                    "Could not find the 'IPython' library. Run 'pip install ipython' to fix this."
                )
            from traitlets.config import Config

            c = Config()
            c.TerminalInteractiveShell.banner1 = banner
            IPython.start_ipython(argv=[], user_ns=context, config=c)
        else:
            code.interact(banner=banner, local=context)
