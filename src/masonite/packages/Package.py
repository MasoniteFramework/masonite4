class Package:
    """Represents a Masonite package and store all elements that can be made available
    to the project (and eventually published in the projet)."""

    name = ""
    base_path = ""
    config_path = ""
    config_name = ""
    commands = {}
    assets = {}
    views = {}
    migrations = []
    routes = {}

    tags = {}

    def has_commands(self):
        return len(self.commands.keys()) > 0

    def has_config(self):
        return self.config_path != ""

    def has_views(self):
        return len(self.views.keys()) > 0

    def has_assets(self):
        return len(self.assets.keys()) > 0

    def has_migrations(self):
        return len(self.migrations) > 0

    def has_routes(self):
        return len(self.routes.keys()) > 0

    def tag(self, part):
        return self.tags[part]

    def set_tag(self, part, tag=None):
        tag = tag if tag else f"{self.name}-{part}"
        self.tags.update({part: tag})
