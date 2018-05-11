from unittest import TestCase
from iclientpy.online import Online
import locale


class TestLocales(TestCase):
    def test_locales(self):
        online = Online()
        if 'zh' in locale.getdefaultlocale()[0]:
            self.assertEqual(online.search_map.__doc__,
                             "\n        查找地图\n        Args:\n            owners: 地图所有者\n            tags: 地图标签\n            keywords: 关键字\n        Returns:\n            简略的地图信息列表\n        ")
        elif 'en' in locale.getdefaultlocale()[0]:
            self.assertEqual(online.search_map.__doc__,
                             "\n        search map\n        Args:\n            owners: map owner\n            tags: map tags\n            keywords: map keywords\n\n        Returns:\n            map info\n        ")
        else:
            self.assertEqual(online.search_map.__doc__,
                             "\n        查找地图\n        Args:\n            owners: 地图所有者\n            tags: 地图标签\n            keywords: 关键字\n        Returns:\n            简略的地图信息列表\n        ")
