from exceptionite.errors import Handler, StackOverflowIntegration, SolutionsIntegration


class ExceptionHandler:
    def __init__(self, application, driver_config=None):
        self.application = application
        self.drivers = {}
        self.driver_config = driver_config or {}
        self.options = {}

    def add_driver(self, name, driver):
        self.drivers.update({name: driver})

    def set_configuration(self, config):
        self.driver_config = config
        return self

    def get_driver(self, name=None):
        if name is None:
            return self.drivers[self.driver_config.get("default")]
        return self.drivers[name]

    def get_config_options(self, driver=None):
        if driver is None:
            return self.driver_config[self.driver_config.get("default")]

        return self.driver_config.get(driver, {})

    def handle(self, exception):
        response = self.application.make("response")
        request = self.application.make("request")
        self.application.make("event").fire(
            f"masonite.exception.{exception.__class__.__name__}", exception
        )

        if self.application.has(f"{exception.__class__.__name__}Handler"):
            return self.application.make(
                f"{exception.__class__.__name__}Handler"
            ).handle(exception)

        handler = Handler(exception)
        handler.integrate(StackOverflowIntegration())
        handler.integrate(SolutionsIntegration())
        handler.context(
            {
                "WSGI": {
                    "Path": request.get_path(),
                    "Input": request.input_bag.all_as_values() or None,
                    # 'Parameters': request.url_params,
                    "Request Method": request.get_request_method(),
                },
                "Headers": request.header_bag.to_dict(),
            }
        )

        return response.view(handler.render(), status=500)
