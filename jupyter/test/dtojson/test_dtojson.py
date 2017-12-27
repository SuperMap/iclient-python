from unittest import TestCase
from iclientpy.dtojson import *


from enum import  Enum

class C(Enum):
    CA = 'CA'

class B:
    b1: str

class A:
    a1: str
    a2: B
    a3: C
    a4: int

a = A()
a.a1 = '1'
a.a2 = B()
a.a2.b1 = 'b1'
a.a4 = 1
a.a3 = C.CA


class TestDTOJson(TestCase):

    def test(self):
        jsonstr = to_json_str(a)
        parseresult = from_json_str(jsonstr, A) # type:A
        self.assertEqual(parseresult.a1, '1')
        self.assertEqual(parseresult.a2.b1, 'b1')
        self.assertEqual(parseresult.a3, C.CA)
        self.assertEqual(parseresult.a4, 1)