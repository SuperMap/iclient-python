from traitlets import HasTraits


class BaseSetting(HasTraits):
    """
    专题图设置的基础类
    """

    def get_settings(self):
        """
        获取设置，metadata通过setttings=true标志的属性

        Returns:
            返回设置
        """
        setting = {}
        for k in [name for name in self.traits(settings=True)]:
            v = getattr(self, k)
            if not v:
                continue
            elif isinstance(v, dict):
                setting[self._underline_to_camel(k)] = self._dict_key_underline_to_camel(v)
            else:
                setting[self._underline_to_camel(k)] = v
        return setting

    def _underline_to_camel(self, underline_format):
        """
        字符串从下划线命名法转为驼峰命名法

        Args:
            underline_format: 以下划线命名法命名的字符串

        Returns:
            驼峰命名法命名的字符串
        """
        if isinstance(underline_format, str):
            split_strs = underline_format.split('_')
            camel_format = split_strs[0]
            for _s_ in split_strs[1:]:
                camel_format += _s_.capitalize()
        else:
            camel_format = underline_format
        return camel_format

    def _dict_key_underline_to_camel(self, source):
        """
        将字典类型数据的key，从下划线命名法转为驼峰命名法

        Args:
            source: 需要转换的字典数据

        Returns:
            key以驼峰命名法的字典
        """
        result = {}
        for k, v in source.items():
            if isinstance(v, dict):
                result[self._underline_to_camel(k)] = self._dict_key_underline_to_camel(v)
            else:
                result[self._underline_to_camel(k)] = v
        return result
