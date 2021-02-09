class DatabaseDriver:
    def __init__(self, application):
        self.application = application

    def set_options(self, options):
        self.options = options
        return self

    def push(self, *jobs):
        builder = (
            self.application.make("builder")
            .on(self.options.get("connection"))
            .table(self.options.get("table"))
        )

    def consume(self, **options):
        pass
