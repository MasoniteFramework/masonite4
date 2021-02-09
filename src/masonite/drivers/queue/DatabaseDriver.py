class DatabaseDriver:
    def __init__(self, application):
        self.application = application

    def set_options(self, options):
        self.options = options
        return self

    def push(self):
        pass

    def consume(self, **options):
        pass
