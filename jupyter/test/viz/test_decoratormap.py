from unittest import TestCase
from iclientpy import heatmap, ranksymbolthememap, honeycombmap, HeatMap, RankSymbolThemeMap, MapvMap


class MapDecoratorTestCase(TestCase):
    def test_heatmap(self):
        map = heatmap([])
        self.assertIsInstance(map, HeatMap)

    def test_ranksymbolthememap(self):
        map = ranksymbolthememap([])
        self.assertIsInstance(map, RankSymbolThemeMap)

    def test_honeycombmap(self):
        map = honeycombmap([])
        self.assertIsInstance(map, MapvMap)
