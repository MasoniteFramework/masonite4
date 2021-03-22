"""Starts Interactive Console Command."""
import code
import sys

from cleo import Command

from ..utils.collections import Collection
from ..utils.structures import load

BANNER = """Masonite Python {} Console
This interactive console has the following things imported:
    container as 'app'
    Collection, load

Type `exit()` to exit."""


class TinkerCommand(Command):
    """
    Run a python shell with the container pre-loaded.

    tinker
        {--i|ipython : Run a IPython shell}
    """

    def handle(self):
        from wsgi import application

        version = "{}.{}.{}".format(
            sys.version_info.major, sys.version_info.minor, sys.version_info.micro
        )
        banner = BANNER.format(version)
        context = {"app": application, "Collection": Collection, "load": load}

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
