from src.masonite.dot import Dot as DictDot
import unittest


class TestDot(unittest.TestCase):
    def test_dict_dot(self):
        self.assertEqual(DictDot().dot("key", {"key": "value"}), "value")
        self.assertEqual(DictDot().dot("key.test", {"key": {"test": "value"}}), "value")
        self.assertEqual(
            DictDot().dot("key.test.layer", {"key": {"test": {"layer": "value"}}}),
            "value",
        )
        self.assertEqual(
            DictDot().dot("key.none", {"key": {"test": {"layer": "value"}}}), None
        )
        self.assertEqual(
            DictDot().dot("key", {"key": {"test": {"layer": "value"}}}),
            {"test": {"layer": "value"}},
        )

    def test_dict_dot_asterisk(self):
        payload = {
            "username": "someone@mail.com",
            "address": [
                {"id": "street1", "street": "some street"},
                {"id": "street2", "street": "a street"},
            ],
        }
        self.assertEqual(DictDot().dot("address.*.id", payload), ["street1", "street2"])
        self.assertEqual(
            DictDot().dot("address.*.street", payload), ["some street", "a street"]
        )
        self.assertEqual(DictDot().dot("user.*.street", payload), [])
        self.assertEqual(DictDot().dot("address.*.house", payload), [])

    def test_dict_dot_asterisk_for_list(self):
        payload = {
            "username": "someone@mail.com",
            "address": [
                {"id": "street1", "street": "some street"},
                {"id": "street2", "street": "a street"},
            ],
            "ages": [1, 2, 3],
        }
        self.assertEqual(DictDot().dot("address.*.id", payload), ["street1", "street2"])
        self.assertEqual(
            DictDot().dot("address.*.street", payload), ["some street", "a street"]
        )
        self.assertEqual(DictDot().dot("user.*.street", payload), [])
        self.assertEqual(DictDot().dot("ages.*", payload), [1, 2, 3])
