"""UpdateTestsTable Migration."""

from masoniteorm.migrations import Migration


class UpdateTestsTable(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table("tests") as table:
            pass

    def down(self):
        """
        Revert the migrations.
        """
        pass
