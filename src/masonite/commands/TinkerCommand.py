"""Starts Interactive Console Command."""
import code
import sys

from cleo import Command

BANNER = """Masonite Python {} Console
This interactive console has the following things imported:
    container as 'app'

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

        if self.option("ipython"):

            try:
                import IPython
            except ImportError:
                raise ModuleNotFoundError(
                    "Could not find the 'IPython' library. Run 'pip install ipython' to fix this."
                )
            from traitlets.config import Config

            c = Config()
            # c.InteractiveShellApp.exec_lines = [
            #     'print("\\nimporting some things\\n")',
            # ]
            c.TerminalInteractiveShell.banner1 = banner
            context = {"app": application}
            IPython.start_ipython(argv=[], user_ns=context, config=c)
        else:
            code.interact(banner=banner, local={"app": application})
