from .Provider import Provider
from whitenoise import WhiteNoise
import os


class WhitenoiseProvider(Provider):
    def __init__(self, application):
        self.application = application

    def register(self):

        response_handler = WhiteNoise(
            self.application.get_response_handler(),
            root=os.path.join(os.getcwd(), "storage"),
            autorefresh=True,
        )

        for location, alias in {
            # folder          # template alias
            "storage/static": "static/",
            "storage/compiled": "static/",
            "storage/uploads": "static/",
            "storage/public": "/",
        }.items():
            response_handler.add_files(location, prefix=alias)

        self.application.bind(
            "response_handler",
            response_handler,
        )

    def boot(self):
        return
