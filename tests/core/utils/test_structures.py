from tests import TestCase

from src.masonite.utils.structures import data_get


class TestStructures(TestCase):
    def test_data_get(self):
        struct = {"key": "val", "a": {"b": "c", "nested": {"a": 1}}}
        self.assertEqual(data_get(struct, "key"), "val")

        self.assertEqual(data_get(struct, "a.b"), "c")
        self.assertEqual(data_get(struct, "a.nested.a"), 1)

        self.assertEqual(data_get(struct, "a.nested.unknown"), None)
        self.assertEqual(data_get(struct, "a.nested.unknown", 0), 0)