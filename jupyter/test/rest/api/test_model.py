import unittest
from iclientpy.rest.api.model import Geometry


class ModelTestCase(unittest.TestCase):
    def test_something(self):
        geo = Geometry()
        self.assertIsNone(geo.points)
        self.assertIsNone(geo.type)
        self.assertIsNone(geo.parts)
        self.assertIsNone(geo.id)
