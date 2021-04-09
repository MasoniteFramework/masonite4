class ValidationExceptionHandler:
    def __init__(self, application):
        self.application = application

    def handle(self, exception):
        errors_bag = exception.errors_bag
        bag_name = exception.bag_name
        # flash into validation bag and use specific name if "bag" given
        if bag_name:
            errors = {bag_name: errors_bag.all()}
        else:
            errors = errors_bag.all()
        self.application.make("session").driver("cookie").flash("errors", errors)

        return self.application.make("response").back()
