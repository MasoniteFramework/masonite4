from os.path import join, basename, isdir, isfile, dirname, realpath

from ..providers import Provider
from ..utils.filesystem import copy_file_or_append
from ..utils.location import config_path
from .Package import Package


class PackageProvider(Provider):

    vendor_prefix = "vendor"
    assets_to = "public"
    part_prefixes = {
        "config": "config",
        "migrations": "migrations",
        "assets": "resources",
        "routes": "routes",
        "views": "templates",
        "commands": "commands",
    }
    routes_variable = "ROUTES"
    # enable_help = False

    # internals
    package = None
    files_to_publish = {"all": {}}

    def configure(self):
        raise NotImplementedError("configure() should be implemented !")

    def register(self):

        self.package = Package()
        self.configure()

        self._check_name()
        self._check_path()
        # TODO: debug as boot not called
        self.boot()

    def publishes(self, tag="all"):
        for source_file, destination_file in self.files_to_publish[tag].items():
            copy_file_or_append(source_file, destination_file)

    def register_for_publishing(self, source_file, destination_file, tag=None):
        if tag:
            self.files_to_publish.update({tag: {source_file: destination_file}})
        else:
            self.files_to_publish["all"].update({source_file: destination_file})

    def boot(self):

        if self.package.has_config():
            self.register_for_publishing(
                self._abs_path(self.package.config_path),
                config_path(self.package.config_name),
            )

        # if self.package.has_commands():
        #     for cmd_name, cmd_class in self.package.commands.items():
        #         self.app.bind(
        #             "{}Command".format(cmd_name.replace("Command", "")),
        #             cmd_class,
        #         )

        # # if self.enable_help:
        # #     self.commands(PackageHelpCommand(self.package))

        # if self.package.has_migrations() and not self._check_migrations_exists():
        #     migrations = [self._abs_path(m) for m in self.package.migrations]
        #     self.publishes_migrations(
        #         migrations,
        #         to=f"databases/migrations/{self._get_package_namespace()}/",
        #         tag=self.package.tag("migrations"),
        #     )

        # if self.package.has_assets():
        #     abs_assets = {
        #         self._abs_path(from_location): to
        #         for (from_location, to) in self.package.assets.items()
        #     }
        #     self.assets(abs_assets)
        #     self.publishes_assets(
        #         abs_assets,
        #         tag=self.package.tag("assets"),
        #     )

        # if self.package.has_routes():
        #     abs_routes = {
        #         self._abs_path(from_location): to
        #         for (from_location, to) in self.package.routes.items()
        #     }
        #     # register different files containing routes
        #     # we must import ROUTES var from each of those abs_routes file
        #     routes = []
        #     for route_file in abs_routes.keys():
        #         # TODO: rewrite when routes will be rewritten
        #         # importlib.import_module("testpackage.routes.web")
        #         # routes_var = getattr(
        #         #     importlib.import_module(f"{self.n}"), self.routes_variable
        #         # )
        #         # routes.append(flatten_routes(routes_var))
        #         pass
        #     self.routes(routes)

        #     # allow publishing of routes
        #     self.publishes(
        #         abs_routes,
        #         tag=self.package.tag("routes"),
        #     )

        # if self.package.has_views():
        #     abs_views = {
        #         self._abs_path(from_location): to
        #         for (from_location, to) in self.package.views.items()
        #     }
        #     # register views
        #     self.views(abs_views)
        #     # define views as publishable
        #     self.publishes(
        #         abs_views,
        #         tag=self.package.tag("views"),
        #     )

    def name(self, name):
        self.package.name = name

    def base_path(self, base_path):
        self.package.base_path = base_path

    # def add_help(self):
    #     self.enable_help = True

    def add_config(self, path, publish_name=""):
        """Define if package have a config file."""
        if publish_name:
            self.package.config_name = publish_name
        else:
            self.package.config_name = path.split(".")[-1]
        abs_path, _ = self._parse_dotted_path(path, publish_name)
        self.package.config_path = self._select_path(abs_path, "config")
        self.application.bind(
            f"config.{self.package.config_name}",
            self._abs_path(self.package.config_path),
        )
        # self.package.set_tag("config", tag)

    # def add_command(self, command, name=""):
    #     """Add a command to register with an optional name. If not given the name of the class will be used."""
    #     command_name = name if name else command.__class__.__name__
    #     self.package.commands.update({command_name: command})

    # def add_commands(self, *commands):
    #     """Add several commands to register. Command name cannot be specified in this mode."""
    #     for command in commands:
    #         self.add_command(command)

    # def add_migration(self, migration, tag=None):
    #     path, _ = self._parse_dotted_path(migration)
    #     migration_path = self._select_path(path, "migrations")
    #     self.package.migrations.append(migration_path)
    #     self.package.set_tag("migrations", tag)

    # def add_migrations(self, *migrations, tag=None):
    #     for migration in migrations:
    #         self.add_migration(migration, tag=tag)
    #     self.package.set_tag("migrations", tag)

    # def add_asset(self, relative_path, publish_name=None, tag=None):
    #     from_relative_path = self._select_path(relative_path, "assets")
    #     name = publish_name if publish_name else basename(relative_path)
    #     to_location = join(self.assets_to, self._get_package_namespace(), name)
    #     self.package.assets.update({from_relative_path: to_location})
    #     self.package.set_tag("assets", tag)

    # def add_assets(self, paths={".": None}, tag=None):
    #     for relative_path, publish_name in paths.items():
    #         self.add_asset(relative_path, publish_name)
    #     self.package.set_tag("assets", tag)

    # def add_routes(self, *routes, tag=None):
    #     for path in routes:
    #         path, name = self._parse_dotted_path(path)
    #         from_path = self._select_path(path, "routes")

    #         self.package.routes.update(
    #             {from_path: join("routes", self._get_package_namespace(), name)}
    #         )
    #     self.package.set_tag("routes", tag)

    # def add_view(self, view_path, publish_name="", tag=None):
    #     path, name = self._parse_dotted_path(view_path, publish_name, ext=".html")
    #     self.package.views.update(
    #         {
    #             self._select_path(path, "views"): join(
    #                 "templates", self._get_package_namespace(), name
    #             )
    #         }
    #     )
    #     self.package.set_tag("views", tag)

    # def add_views(self, *views, tag=None):
    #     for view in views:
    #         self.add_view(view)
    #     self.package.set_tag("views", tag)

    def _get_package_namespace(self):
        return join(self.vendor_prefix, self.package.name)

    def _check_name(self):
        if not self.package.name:
            raise NotImplementedError("package 'name' should be defined !")
        # if "masonite" in self.package.name:
        #     warnings.warn("'name' in PackageProvider should not contains 'masonite'")

    def _check_path(self):
        if not self.package.base_path:
            raise NotImplementedError("package root 'path' should be defined !")

    # def _check_migrations_exists(self):
    #     # TODO: should we really check this ?
    #     pass

    def _abs_path(self, relative_path):
        return join(self.package.base_path, relative_path)

    def _parse_dotted_path(self, dotted_path, override_name="", ext=".py"):
        # TODO: make some validations (no / and no py)
        if dotted_path.endswith(ext) or "/" in dotted_path:
            raise ValueError(
                "The input path must be a dotted path without .py extension"
            )
        if override_name.endswith(ext) or "." in override_name:
            raise ValueError(
                "The name override must be a simple name without .py extension"
            )
        if override_name:
            name = override_name
        else:
            name = basename(dotted_path).split(".")[-1]
        filename = f"{name}{ext}"
        relative_path = dotted_path.replace(".", "/") + ext
        return relative_path, filename

    def _select_path(self, path, part):
        """This will check if path in classic folder for the given part exists and will build the relative path.
        If not this build the relative path from package root.
        Example: my_settings.py, config => will return ./config/my_settings.py if exists else ./my_settings.py
        """
        classic_path = join(self.part_prefixes[part], path)
        # look first in "package" convention location if file or folder exists
        abs_path = join(self.package.base_path, classic_path)
        if not isfile(abs_path) and not isdir(abs_path):
            return path
        else:
            return classic_path

    # def _get_abs_path_dot(self, relative_path, part, ext="py"):
    #     # add extensions
    #     if "." in relative_path:
    #         # resolve given path
    #         path = load(relative_path)
    #     else:
    #         # look first in "package" convention location
    #         basename = (f"{relative_path}.{ext}",)
    #         path = join(self.package.base_path, self.part_prefixes[part], basename)
    #         if not isfile(path) and not isdir(path):
    #             # else look at root
    #             path = join(self.package.base_path, basename)
    #     # TODO: should we check here to returns human exception ?
    #     return path