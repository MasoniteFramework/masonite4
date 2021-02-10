"""New Key Command."""
from cleo import Command


class QueueWorkCommand(Command):
    """
    Generate a new key.

    queue:work
        {--c|--connection : Specifies the database connection if using database driver.}
        {--queue=default : The queue to listen to}
        {--d|driver=None : Specify the driver you would like to connect to}
        {--p|poll=0 : Specify the frequency a worker should poll}
        {--failed : Run only the failed jobs}
    """

    def __init__(self, application):
        super().__init__()
        self.app = application

    def handle(self):
        driver = self.option("driver")
        if driver == "None":
            driver = None

        print(
            self.app.make("queue").consume(
                {
                    "driver": driver,
                }
            )
        )
