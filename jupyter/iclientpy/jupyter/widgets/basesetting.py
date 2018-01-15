from traitlets import HasTraits


class BaseSetting(HasTraits):
    def get_settings(self):
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
        :type source:dict
        :type result:dict
        """
        result = {}
        for k, v in source.items():
            if isinstance(v, dict):
                result[self._underline_to_camel(k)] = self._dict_key_underline_to_camel(v)
            else:
                result[self._underline_to_camel(k)] = v
        return result
