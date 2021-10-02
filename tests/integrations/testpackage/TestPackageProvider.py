from os.path import dirname, realpath
from src.masonite.packages import PackageProvider


class TestPackageProvider(PackageProvider):
    def __init__(self, application):
        self.application = application

    def configure(self):
        self.name("test-package")
        self.base_path(dirname(realpath(__file__)))
        self.add_config(
            "params", publish_name="package"
        )  # optional name else inferred from package name
