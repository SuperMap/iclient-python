from iclientpy.typeassert import typeassert
from unittest import TestCase
from typing import List
from enum import Enum


class Operater(Enum):
    ADD = 'ADD'
    SUB = 'SUB'


class TypeAssertTestCase(TestCase):
    @typeassert
    def add(self, x: int, y: int):
        return x + y

    @typeassert
    def compute_sum(self, items: List[int]):
        return sum(items)

    @typeassert
    def compute(self, x: int, y: int, operater: Operater):
        result = 0
        if operater is Operater.ADD:
            result = x + y
        elif operater is Operater.SUB:
            result = x - y
        return result

    def test_add(self):
        result = self.add(3, 4)
        self.assertEqual(result, 7)

    def test_add_failed(self):
        with self.assertRaises(TypeError) as context:
            self.add(3, '4')
        self.assertEqual("Argument y must be <class 'int'>", str(context.exception))

    def test_compute_sum_list(self):
        result = self.compute_sum([1, 2, 3])
        self.assertEqual(result, 6)

    def test_compute_sum_failed(self):
        with self.assertRaises(TypeError) as context:
            self.compute_sum(3)
        self.assertEqual("Argument items must be typing.List[int]", str(context.exception))

    def test_compute(self):
        result = self.compute(4, 3, Operater.ADD)
        self.assertEqual(result, 7)
        result = self.compute(4, 3, Operater.SUB)
        self.assertEqual(result, 1)

    def test_compute_failed(self):
        with self.assertRaises(TypeError) as context:
            self.compute(4, 3, 'ADD')
        self.assertEqual("Argument operater must be <enum 'Operater'>", str(context.exception))
