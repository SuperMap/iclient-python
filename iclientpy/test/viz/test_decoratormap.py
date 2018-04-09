from unittest import TestCase
from iclientpy import heat, ranksymboltheme, honeycomb, geolines, GeoLines, HeatMap, RankSymbolThemeMap, MapvMap


class MapDecoratorTestCase(TestCase):
    def test_heatmap(self):
        map = heat([])
        self.assertIsInstance(map, HeatMap)

    def test_ranksymbolthememap(self):
        map = ranksymboltheme([])
        self.assertIsInstance(map, RankSymbolThemeMap)

    def test_honeycombmap(self):
        map = honeycomb([])
        self.assertIsInstance(map, MapvMap)

    def test_geolines(self):
        map = geolines([])
        self.assertIsInstance(map, GeoLines)
