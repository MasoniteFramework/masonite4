"""Publish elements from a package"""
from cleo import Command

from ..packages import PackageProvider


class PublishCommand(Command):
    """
    Publishes a package
    publish
        {name : Name of the package you want to publish}
        {--t|tag=all : The tag of the specific elemenet you want to publish}
    """

    def __init__(self, application):
        super().__init__()
        self.app = application

    def handle(self):
        # TODO: try to found the package provider for the given package name
        # MyPackageProvider => name "my-package" => craft publish my-package
        # self.app.providers.get(self.argument("name"))
        name = self.argument("name")
        package_provider = None
        for provider in self.app.providers:
            if isinstance(provider, PackageProvider) and provider.package.name == name:
                package_provider = provider
        if not package_provider:
            raise ValueError(f"Could not find the package provider for {name}")

        tag = self.option("tag")
        # TODO:
        import pdb

        pdb.set_trace()
        package_provider.publishes(tag=tag)
        # package_provider.publish_migrations(tag=tag)
        # package_provider.publish_assets(tag=tag)
