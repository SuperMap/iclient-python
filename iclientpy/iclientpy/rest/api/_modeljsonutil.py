from typing import Dict
from iclientpy.dtojson import AbstractTypeParserSwitcher,register, parser


class AbstractTypeParserSwitcherBuilder:
    _clz: type
    _field_name: str
    _parsers: {}
    def __init__(self, clz: type, field_name: str):
        self._clz = clz
        #TODO 检查字段名字是否正确
        self._field_name = field_name
        self._parsers = {}

    def __call__(self, *field_values):
        def wrap(sub_class: type):
            sub_class_parser = parser(sub_class)
            for field_value in field_values:
                self._parsers[field_value] = parser(sub_class)
            return sub_class
        return wrap

    def build_and_regist(self):
        register(self._clz, AbstractTypeParserSwitcher(self._field_name, self._parsers, parser(self._clz)))
