import unittest

from lanka_travel import Route


class TestCase(unittest.TestCase):

    def test_list_all(self):
        Route.list_all()
