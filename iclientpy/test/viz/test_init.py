from unittest import TestCase
from functools import wraps
from iclientpy.viz import build_parameter_class


class A:
    def __init__(self, *args, **kwargs):
        print(args)
        for k, v in kwargs.items():
            setattr(self, k, v)


class InitTestCase(TestCase):
    def test_method_parameter_class(self):
        def asser_func(func):
            @wraps(func)
            def wrap_func(*args, **kwargs):
                self.assertIsNotNone(kwargs)
                a = kwargs['a']  #:type A
                self.assertIs(a.b, 2)
                self.assertIs(a.c, 3)

            return wrap_func

        @build_parameter_class(A, clz_field_name="a", fields=['b', 'c'])
        @asser_func
        def func(*, b, c):
            pass

        func(b=2, c=3)
