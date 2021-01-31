from ..foundation import response_handler


class WSGIProvider:
    def __init__(self, app):
        self.application = app

    def register(self):
        self.application.set_response_handler(response_handler)

    def boot(self):
        pass
