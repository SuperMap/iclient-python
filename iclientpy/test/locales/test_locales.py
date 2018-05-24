from unittest import TestCase
from iclientpy.online import Online
import locale


class TestLocales(TestCase):
    def test_module(self):
        online = Online()
        if 'zh' in locale.getdefaultlocale()[0]:
            import iclientpy.locales.iclientpy_zh as loc
            self.assertEqual(online.search_map.__doc__, loc.iclientpy_locale.get("iclientpy.online.Online.search_map"))
        elif 'en' in locale.getdefaultlocale()[0]:
            import iclientpy.locales.iclientpy_en as loc
            self.assertEqual(online.search_map.__doc__, loc.iclientpy_locale.get("iclientpy.online.Online.search_map"))
        else:
            import iclientpy.locales.iclientpy as loc
            self.assertEqual(online.search_map.__doc__, loc.iclientpy_locale.get("iclientpy.online.Online.search_map"))
