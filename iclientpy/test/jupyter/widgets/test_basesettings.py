import unittest
from traitlets import Unicode, Dict, default
from iclientpy.jupyter.widgets.basesetting import BaseSetting


class BaseSettingTestCase(unittest.TestCase):
    def test_test_setting(self):
        setting = SubSetting(pro_str_1='str1', pro_str_2="str2")
        setting_dict = setting.get_settings()
        self.assertEqual(setting_dict['proStr1'], 'str1')
        self.assertEqual(setting_dict['sub']['proStr2'], 'str2')

    def test_test_setting_2(self):
        setting = SubSetting(pro_str_1='str1')
        setting_dict = setting.get_settings()
        self.assertEqual(setting_dict['proStr1'], 'str1')
        self.assertTrue('sub' not in setting_dict)


class SubSetting(BaseSetting):
    pro_str_1 = Unicode().tag(settings=True)
    pro_str_2 = Unicode().tag(sub=True)
    sub = Dict().tag(settings=True)

    @default('sub')
    def _default_sub(self):
        tmp_sub = {}
        for name in self.traits(sub=True):
            v = getattr(self, name)
            if not v:
                continue
            tmp_sub[name] = v
        return tmp_sub
