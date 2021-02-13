"""Queue Work Command."""
from cleo import Command


class QueueWorkCommand(Command):
    """
    Creates a new queue worker to consume queue jobs

    queue:work
        {--c|--connection : Specifies the database connection if using database driver.}
        {--queue=default : The queue to listen to}
        {--d|driver=None : Specify the driver you would like to use}
        {--p|poll=1 : Specify the seconds a worker should wait before fetching new jobs}
        {--attempts=None : Specify the number of times a job should be retried before it fails}
    """

    def __init__(self, application):
        super().__init__()
        self.app = application

    def handle(self):
        options = {}
        driver = None if driver == "None" else self.option("driver")

        options.update({"driver": driver})
        if self.option("poll") != "None":
            options.update({"poll": self.option("poll")})

        attempts = self.option("attempts")
        if attempts == "None":
            attempts = None
        else:
            options.update({"attempts": attempts})

        return self.app.make("queue").consume(options)
