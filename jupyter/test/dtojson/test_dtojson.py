from unittest import TestCase
from iclientpy.dtojson import *
import typing
import inspect

from enum import  Enum

class C(Enum):
    CA = 'CA'
    CB = 'CB'
    CC = 'CC'

class B:
    b1: str

class A:
    a1: str
    a2: B
    a3: C
    a4: int
    a5: typing.List[C]

a = A()
a.a1 = '1'
a.a2 = B()
a.a2.b1 = 'b1'
a.a4 = 1
a.a3 = C.CA
a.a5 = [C.CA, C.CB]
class TestDTOJson(TestCase):

    def test(self):
        jsonstr = to_json_str(a)
        parseresult = from_json_str(jsonstr, A) # type:A
        self.assertEqual(parseresult.a1, '1')
        self.assertEqual(parseresult.a2.b1, 'b1')
        self.assertEqual(parseresult.a3, C.CA)
        self.assertEqual(parseresult.a4, 1)
        self.assertIn(C.CA, parseresult.a5)
        self.assertIn(C.CB, parseresult.a5)
        self.assertNotIn(C.CC, parseresult.a5)


    def testArray(self) -> typing.List[C]:
        annos = inspect.getfullargspec(self.testArray).annotations
        list = from_json_str('["CA","CB"]', annos['return'])
        self.assertEqual(len(list), 2)

    def testDictProperty(self):
        class WithDictProp:
            dictProp: dict
        parseresult = from_json_str('{"dictProp":{"key":"value"}}', WithDictProp) # type:WithDictProp
        self.assertEqual(parseresult.dictProp['key'], 'value')

        to_parse = WithDictProp()
        to_parse.dictProp = {"key":"value"}
        jsonstr = to_json_str(to_parse)
        self.assertIn('{"key":"value"}', jsonstr.replace(' ', '', 3))
