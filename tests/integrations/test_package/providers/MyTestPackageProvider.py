from src.masonite.packages.providers import PackageProvider
from tests.integrations.test_package.commands.Command1 import Command1
from tests.integrations.test_package.commands.Command2 import Command2


class MyTestPackageProvider(PackageProvider):
    def configure(self):
        (
            self.root("tests/integrations/test_package")
            .name("test_package")
            .add_config("config/test.py", publish=True)
            .add_views("templates", publish=True)
            .add_commands(Command1(), Command2())
            .add_migrations("migrations/create_some_table.py")
            # .add_routes("routes/api.py", "routes/web.py")
            .add_assets("assets")
        )
