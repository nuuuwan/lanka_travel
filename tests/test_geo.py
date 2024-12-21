import unittest

from lanka_travel import Geo
from utils_future import LatLng


class TestCase(unittest.TestCase):
    @unittest.skip("slow")
    def test_get_region_id(self):
        self.assertEqual(
            Geo().get_region_id(LatLng(6.917272, 79.864795)),
            "LK-11",
        )
