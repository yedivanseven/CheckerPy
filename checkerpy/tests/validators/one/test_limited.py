import logging
import unittest as ut
from ....validators.one import Limited
from ....exceptions import WrongTypeError, LimitError, CallableError
from ....types.one import _COMPARABLES
from ....functional import CompositionOf


class TestLimited(ut.TestCase):

    def test_works_with_sane_bool(self):
        out = Limited(False, lo=False, hi=True)
        self.assertIsInstance(out, bool)
        self.assertEqual(out, False)

    def test_works_with_sane_int(self):
        out = Limited(2, lo=1, hi=3)
        self.assertIsInstance(out, int)
        self.assertEqual(out, 2)

    def test_works_with_sane_float(self):
        out = Limited(2.0, lo=1, hi=3)
        self.assertIsInstance(out, float)
        self.assertEqual(out, 2.0)

    def test_works_with_sane_str(self):
        out = Limited('b', lo='a', hi='c')
        self.assertIsInstance(out, str)
        self.assertEqual(out, 'b')

    def test_works_with_sane_tuple(self):
        out = Limited((2, 3), lo=(1, 2), hi=(3, 4))
        self.assertIsInstance(out, tuple)
        self.assertTupleEqual(out, (2, 3))

    def test_works_with_sane_list(self):
        out = Limited([2, 3], lo=[1, 2], hi=[3, 4])
        self.assertIsInstance(out, list)
        self.assertListEqual(out, [2, 3])

    def test_works_with_sane_set(self):
        out = Limited({2, 3}, lo={1, 2}, hi={3, 4})
        self.assertIsInstance(out, set)
        self.assertSetEqual(out, {2, 3})

    def test_error_on_unnamed_value_uncomparable_to_lower_limit(self):
        log_msg = ['ERROR:root:Cannot compare type str of '
                   'foo with limits of types int and ellipsis!']
        err_msg = ('Cannot compare type str of foo '
                   'with limits of types int and ellipsis!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = Limited('foo', lo=1)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_value_uncomparable_to_lower_limit(self):
        log_msg = ['ERROR:root:Cannot compare type str of '
                   'test with limits of types int and ellipsis!']
        err_msg = ('Cannot compare type str of test '
                   'with limits of types int and ellipsis!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = Limited('bar', 'test', lo=1)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_unnamed_value_uncomparable_to_higher_limit(self):
        log_msg = ['ERROR:root:Cannot compare type str of '
                   'foo with limits of types ellipsis and int!']
        err_msg = ('Cannot compare type str of foo '
                   'with limits of types ellipsis and int!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = Limited('foo', hi=2)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_value_uncomparable_to_higher_limit(self):
        log_msg = ['ERROR:root:Cannot compare type str of '
                   'test with limits of types ellipsis and int!']
        err_msg = ('Cannot compare type str of test '
                   'with limits of types ellipsis and int!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = Limited('bar', 'test', hi=2)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_unnamed_value_uncomparable_to_limits(self):
        log_msg = ['ERROR:root:Cannot compare type str of '
                   'foo with limits of types float and int!']
        err_msg = ('Cannot compare type str of foo '
                   'with limits of types float and int!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = Limited('foo', lo=1.0, hi=2)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_value_uncomparable_to_limits(self):
        log_msg = ['ERROR:root:Cannot compare type str of '
                   'test with limits of types float and int!']
        err_msg = ('Cannot compare type str of test '
                   'with limits of types float and int!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = Limited('bar', 'test', lo=1.0, hi=2)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_unnamed_variable_out_bounds(self):
        log_msg = ['ERROR:root:Value 0 lies outside '
                   'the allowed interval [1.0, 2]!']
        err_msg = 'Value 0 lies outside the allowed interval [1.0, 2]!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LimitError) as err:
                _ = Limited(0, lo=1.0, hi=2)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_variable_out_bounds(self):
        log_msg = ['ERROR:root:Value 0 of test lies outside '
                   'the allowed interval [1.0, 2]!']
        err_msg = 'Value 0 of test lies outside the allowed interval [1.0, 2]!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LimitError) as err:
                _ = Limited(0, 'test', lo=1.0, hi=2)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_out_of_bounds_error_with_lower_limit_None(self):
        log_msg = ['ERROR:root:Value 3 lies outside '
                   'the allowed interval (-inf, 2]!']
        err_msg = 'Value 3 lies outside the allowed interval (-inf, 2]!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LimitError) as err:
                _ = Limited(3, hi=2)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_out_of_bounds_error_with_lower_limit_inf(self):
        log_msg = ['ERROR:root:Value 3 lies outside '
                   'the allowed interval (-inf, 2]!']
        err_msg = 'Value 3 lies outside the allowed interval (-inf, 2]!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LimitError) as err:
                _ = Limited(3, lo=float('-inf'), hi=2)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_out_of_bounds_error_with_upper_limit_None(self):
        log_msg = ['ERROR:root:Value 0 lies outside '
                   'the allowed interval [1.0, inf)!']
        err_msg = 'Value 0 lies outside the allowed interval [1.0, inf)!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LimitError) as err:
                _ = Limited(0, lo=1.0)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_out_of_bounds_error_with_upper_limit_inf(self):
        log_msg = ['ERROR:root:Value 0 lies outside '
                   'the allowed interval [1.0, inf)!']
        err_msg = 'Value 0 lies outside the allowed interval [1.0, inf)!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LimitError) as err:
                _ = Limited(0, lo=1.0, hi=float('inf'))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_has_comparable_type_checker_attributes(self):
        for comparable in _COMPARABLES:
            self.assertTrue(hasattr(Limited, comparable.__name__))

    def test_iterable_type_checkers_are_type_CompositionOf(self):
        for comparable in _COMPARABLES:
            type_checker = getattr(Limited, comparable.__name__)
            self.assertIsInstance(type_checker, CompositionOf)

    def test_has_attribute_NonEmpty(self):
        self.assertTrue(hasattr(Limited, 'NonEmpty'))

    def test_attribute_NonEmpty_is_type_CompositionOf(self):
        self.assertIsInstance(Limited.NonEmpty, CompositionOf)

    def test_hi_and_lo_are_passed_through_type_checker(self):
        log_msg = ['ERROR:root:Value 0 lies outside '
                   'the allowed interval [1.0, 2]!']
        err_msg = 'Value 0 lies outside the allowed interval [1.0, 2]!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LimitError) as err:
                _ = Limited.JustInt(0, lo=1.0, hi=2)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_has_attribute_o(self):
        self.assertTrue(hasattr(Limited, 'o'))

    def test_attribute_o_is_callable(self):
        self.assertTrue(callable(Limited.o))

    def test_o_returns_composition(self):
        def f(x):
            return x
        composition = Limited.o(f)
        self.assertIsInstance(composition, CompositionOf)

    def test_o_raises_error_on_argument_not_callable(self):
        err_msg = ('foo must be a callable that accepts (i) a value,'
                   ' (ii) an optional name for that value, and (iii)'
                   ' any number of keyword arguments!')
        with self.assertRaises(CallableError) as err:
            _ = Limited.o('foo')
        self.assertEqual(str(err.exception), err_msg)



if __name__ == '__main__':
    ut.main()
