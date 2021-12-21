"""New Model Command."""
from cleo import Command
from inflection import tableize, camelize
import os

from ..utils.filesystem import make_directory, render_stub_file, get_module_dir
from ..utils.str import as_filepath
from ..utils.location import base_path, migrations_path


class MakeModelCommand(Command):
    """
    Creates a new model class.

    model
        {name : Name of the model}
        {--m|migration : Optionally create a migration file}
        {--c|create : If the migration file should create a table}
        {--t|table : If the migration file should modify an existing table}
    """

    def __init__(self, application):
        super().__init__()
        self.app = application

    def handle(self):
        name = camelize(self.argument("name"))
        content = render_stub_file(self.get_models_path(), name)

        relative_filename = os.path.join(
            as_filepath(self.app.make("models.location")), name + ".py"
        )
        filepath = base_path(relative_filename)
        make_directory(filepath)

        with open(filepath, "w") as f:
            f.write(content)

        self.info(f"Model Created ({relative_filename})")

        if self.option("migration"):
            if self.option("create"):
                self.call(
                    "migration",
                    f"create_{tableize(name)}_table --create {tableize(name)} --directory {migrations_path()}",
                )
            else:
                self.call(
                    "migration",
                    f"update_{tableize(name)}_table --table {tableize(name)} --directory {migrations_path()}",
                )

    def get_models_path(self):
        return os.path.join(get_module_dir(__file__), "../stubs/models/Model.py")
