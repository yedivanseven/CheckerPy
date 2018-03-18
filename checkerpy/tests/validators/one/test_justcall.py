import logging
import unittest as ut
from ....validators.one import JustCall
from ....exceptions import CallableError
from ....functional import CompositionOf


class TestJustCall(ut.TestCase):

    def test_works_with_sane_callable(self):
        inp = lambda x: x
        out = JustCall(inp)
        self.assertIs(out, inp)

    def test_error_on_unnamed_object_without_name_attr(self):
        log_msg = ['ERROR:root:Object foo of type str is not callable!']
        err_msg = 'Object foo of type str is not callable!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(CallableError) as err:
                _ = JustCall('foo')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_object_without_name_attr(self):
        log_msg = ['ERROR:root:Object test of type int is not callable!']
        err_msg = 'Object test of type int is not callable!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(CallableError) as err:
                _ = JustCall(1, 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_unnamed_object_with_name_attr(self):
        class Test:
            pass
        t = Test()
        t.__name__= 'test'
        log_msg = ['ERROR:root:Object test of type Test is not callable!']
        err_msg = 'Object test of type Test is not callable!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(CallableError) as err:
                _ = JustCall(t)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_object_with_name_attr(self):
        class Test:
            pass
        t = Test()
        t.__name__= 'test'
        log_msg = ['ERROR:root:Object name of type Test is not callable!']
        err_msg = 'Object name of type Test is not callable!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(CallableError) as err:
                _ = JustCall(t, 'name')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_has_attribute_o(self):
        self.assertTrue(hasattr(JustCall, 'o'))

    def test_attribute_o_is_callable(self):
        self.assertTrue(callable(JustCall.o))

    def test_o_returns_composition(self):
        def f(x):
            return x
        composition = JustCall.o(f)
        self.assertIsInstance(composition, CompositionOf)

    def test_o_raises_error_on_argument_not_callable(self):
        err_msg = ('foo must be a callable that accepts (i) a value,'
                   ' (ii) an optional name for that value, and (iii)'
                   ' any number of keyword arguments!')
        with self.assertRaises(CallableError) as err:
            _ = JustCall.o('foo')
        self.assertEqual(str(err.exception), err_msg)


if __name__ == '__main__':
    ut.main()
