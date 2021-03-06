import time
import os
import sys

import hupper
import waitress
from cleo import Command


class ServeCommand(Command):
    """
    Run the Masonite server.

    serve
        {--p|port=8000 : Specify which port to run the server}
        {--b|host=127.0.0.1 : Specify which ip address to run the server}
        {--r|reload : Make the server automatically reload on file changes}
        {--d|dont-reload : Make the server NOT automatically reload on file changes}
        {--i|reload-interval=1 : Number of seconds to wait to reload after changed are detected}
        {--l|live-reload : Make the server automatically refresh your web browser}
    """

    def handle(self):
        if self.option("live-reload"):
            try:
                from livereload import Server
            except ImportError:
                raise ImportError(
                    "Could not find the livereload library. Install it by running 'pip install livereload==2.5.1'"
                )

            from wsgi import application
            import glob

            server = Server(application)
            for filepath in glob.glob("resources/templates/**/*/"):
                server.watch(filepath)

            self.line("")
            self.info("Live reload server is starting...")
            self.info(
                "This will only work for templates. Changes to Python files may require a browser refresh."
            )
            self.line("")
            application = server.serve(
                port=self.option("port"),
                restart_delay=self.option("reload-interval"),
                liveport=5500,
                root=application.base_path,
                debug=True,
            )
            return

        reloader = hupper.start_reloader("src.masonite.commands.ServeCommand.main")

        # monitor an extra file
        reloader.watch_files([".env", application.get_storage_path()])


def main(args=sys.argv[1:]):
    from wsgi import application

    host = "127.0.0.1"
    port = "8000"
    if "--host" in args:
        host = args[args.index("--host") + 1]
    if "--port" in args:
        port = args[args.index("--host") + 1]
    if "-p" in args:
        port = args[args.index("-p") + 1]

    waitress.serve(application, host=host, port=port)
