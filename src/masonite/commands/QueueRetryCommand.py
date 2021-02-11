"""New Key Command."""
from cleo import Command


class QueueRetryCommand(Command):
    """
    Generate a new key.

    queue:retry
        {--c|--connection=default : Specifies the database connection if using database driver.}
        {--queue=default : The queue to listen to}
        {--d|driver=None : Specify the driver you would like to connect to}
    """

    def __init__(self, application):
        super().__init__()
        self.app = application

    def handle(self):
        driver = self.option("driver")
        if driver == "None":
            driver = None

        return self.app.make("queue").retry(
            {
                "driver": driver,
                "connection": self.option("connection"),
                "queue": self.option("queue"),
            }
        )
