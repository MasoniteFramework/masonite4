class PresenceChannel:
    def __init__(self, name):
        if not name.startswith("presence-"):
            name = "presence-" + name

        self.name = name

    def authorized(self, application):
        return (
            application.make("router")
            .find_by_name("broadcasting.authorize")
            .get_response()
        )
