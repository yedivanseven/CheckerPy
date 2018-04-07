import logging
import unittest as ut
from ....functional import CompositionOf
from ....validators.all import LimitedTuple
from ....exceptions import LenError, WrongTypeError, LimitError, CallableError
from ....types.all import _ALL_COMPARABLES, TypedDict


class TestLimitedTupleLimits(ut.TestCase):

    def test_error_on_limits_not_tuple(self):
        err_msg = 'Type of limits must be tuple, not int like 1!'
        with self.assertRaises(TypeError) as err:
            _ = LimitedTuple((1, 3, 4), limits=1)
        self.assertEqual(str(err.exception), err_msg)

    def test_error_on_limits_named_type(self):
        err_msg = 'Type of limits must be tuple, not frozenset!'
        with self.assertRaises(TypeError) as err:
            _ = LimitedTuple((1, 3, 4), limits=frozenset({2}))
        self.assertEqual(str(err.exception), err_msg)

    def test_error_on_limit_not_tuple(self):
        err_msg = 'Type of limits on argument 1 must be tuple, not int like 2!'
        with self.assertRaises(TypeError) as err:
            _ = LimitedTuple((1, 2), limits=((0, 3), 2))
        self.assertEqual(str(err.exception), err_msg)

    def test_error_on_limit_named_type(self):
        err_msg = 'Type of limits on argument 1 must be tuple, not frozenset!'
        with self.assertRaises(TypeError) as err:
            _ = LimitedTuple((1, 2), limits=((0, 3), frozenset({2})))
        self.assertEqual(str(err.exception), err_msg)

    def test_error_on_limit_length_not_2(self):
        err_msg = ('There must be exactly 2 limits (lo'
                   ' and hi) for argument 1, not 3!')
        with self.assertRaises(ValueError) as err:
            _ = LimitedTuple((1, 2), limits=((0, 3), (1, 2, 3)))
        self.assertEqual(str(err.exception), err_msg)

    def test_works_with_all_limits_set(self):
        inp = (1, 2)
        out = LimitedTuple(inp, limits=((0, 2), (1, 3)))
        self.assertTupleEqual(out, inp)

    def test_works_with_one_ellipsis_in_limit(self):
        inp = (1, 2)
        out = LimitedTuple(inp, limits=((0, 2), (..., 3)))
        self.assertTupleEqual(out, inp)

    def test_works_with_two_ellipsis_in_limit(self):
        inp = (1, 2)
        out = LimitedTuple(inp, limits=((0, 2), (..., ...)))
        self.assertTupleEqual(out, inp)

    def test_works_with_ellipsis_instead_of_limit(self):
        inp = (1, 2, 3)
        out = LimitedTuple(inp, limits=((0, 2), ..., (2, 4)))
        self.assertTupleEqual(out, inp)


class TestLimitedTupleValue(ut.TestCase):

    def test_works_with_empty_tuple(self):
        out = LimitedTuple(())
        self.assertTupleEqual(out, ())

    def test_error_on_unnamed_tuple_wrong_length(self):
        inp = (1, 'foo', True)
        log_msg = ["ERROR:root:Length of tuple (1, "
                   "'foo', True) must be 2, not 3!"]
        err_msg = "Length of tuple (1, 'foo', True) must be 2, not 3!"
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = LimitedTuple(inp, limits=((0, 2), (1, 3)))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_tuple_wrong_length(self):
        inp = (1, 'foo', True)
        log_msg = ['ERROR:root:Length of tuple test must be 2, not 3!']
        err_msg = 'Length of tuple test must be 2, not 3!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = LimitedTuple(inp, 'test', limits=((0, 2), (1, 3)))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_element_of_unnamed_tuple_out_of_bounds(self):
        inp = (1, 2)
        log_msg = ['ERROR:root:Value 2 of element 1 in tuple (1, '
                   '2) lies outside the allowed interval [3, 5]!']
        err_msg = ('Value 2 of element 1 in tuple (1, 2) lies'
                   ' outside the allowed interval [3, 5]!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LimitError) as err:
                _ = LimitedTuple(inp, limits=((0, 2), (3, 5)))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_element_of_named_tuple_out_of_bounds(self):
        inp = (1, 2)
        log_msg = ['ERROR:root:Value 2 of element 1 in tuple test'
                   ' lies outside the allowed interval [3, 5]!']
        err_msg = ('Value 2 of element 1 in tuple test lies'
                   ' outside the allowed interval [3, 5]!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LimitError) as err:
                _ = LimitedTuple(inp, 'test', limits=((0, 2), (3, 5)))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_element_of_unnamed_tuple_uncomparable(self):
        inp = (1, 2)
        log_msg = ['ERROR:root:Cannot compare type int of element 1 '
                   'in tuple (1, 2) with limits of types str and str!']
        err_msg = ('Cannot compare type int of element 1 in tuple'
                   ' (1, 2) with limits of types str and str!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = LimitedTuple(inp, limits=((0, 2), ('a', 'b')))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_element_of_named_tuple_uncomparable(self):
        inp = (1, 2)
        log_msg = ['ERROR:root:Cannot compare type int of element 1 '
                   'in tuple test with limits of types str and str!']
        err_msg = ('Cannot compare type int of element 1 in tuple'
                   ' test with limits of types str and str!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = LimitedTuple(inp, 'test', limits=((0, 2), ('a', 'b')))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_out_of_bounds_error_on_element_of_unnamed_tuple_lower_bound(self):
        inp = (1, 2)
        log_msg = ['ERROR:root:Value 2 of element 1 in tuple (1, '
                   '2) lies outside the allowed interval [3, inf)!']
        err_msg = ('Value 2 of element 1 in tuple (1, 2) lies'
                   ' outside the allowed interval [3, inf)!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LimitError) as err:
                _ = LimitedTuple(inp, limits=((0, 2), (3, ...)))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_out_of_bounds_error_on_element_of_named_tuple_lower_bound(self):
        inp = (1, 2)
        log_msg = ['ERROR:root:Value 2 of element 1 in tuple test'
                   ' lies outside the allowed interval [3, inf)!']
        err_msg = ('Value 2 of element 1 in tuple test lies'
                   ' outside the allowed interval [3, inf)!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LimitError) as err:
                _ = LimitedTuple(inp, 'test', limits=((0, 2), (3, ...)))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_out_of_bounds_error_on_element_of_unnamed_tuple_upper_bound(self):
        inp = (1, 2)
        log_msg = ['ERROR:root:Value 2 of element 1 in tuple (1, '
                   '2) lies outside the allowed interval (-inf, 1]!']
        err_msg = ('Value 2 of element 1 in tuple (1, 2) lies'
                   ' outside the allowed interval (-inf, 1]!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LimitError) as err:
                _ = LimitedTuple(inp, limits=((0, 2), (..., 1)))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_out_of_bounds_error_on_element_of_named_tuple_upper_bound(self):
        inp = (1, 2)
        log_msg = ['ERROR:root:Value 2 of element 1 in tuple test'
                   ' lies outside the allowed interval (-inf, 1]!']
        err_msg = ('Value 2 of element 1 in tuple test lies'
                   ' outside the allowed interval (-inf, 1]!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LimitError) as err:
                _ = LimitedTuple(inp, 'test', limits=((0, 2), (..., 1)))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_element_of_unnamed_tuple_uncomparable_lower_bound(self):
        inp = (1, 2)
        log_msg = ['ERROR:root:Cannot compare type int of element 1 in '
                   'tuple (1, 2) with limits of types str and ellipsis!']
        err_msg = ('Cannot compare type int of element 1 in tuple '
                   '(1, 2) with limits of types str and ellipsis!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = LimitedTuple(inp, limits=((0, 2), ('a', ...)))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_element_of_named_tuple_uncomparable_lower_bound(self):
        inp = (1, 2)
        log_msg = ['ERROR:root:Cannot compare type int of element 1 in'
                   ' tuple test with limits of types str and ellipsis!']
        err_msg = ('Cannot compare type int of element 1 in tuple'
                   ' test with limits of types str and ellipsis!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = LimitedTuple(inp, 'test', limits=((0, 2), ('a', ...)))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_element_of_unnamed_tuple_uncomparable_upper_bound(self):
        inp = (1, 2)
        log_msg = ['ERROR:root:Cannot compare type int of element 1 in '
                   'tuple (1, 2) with limits of types ellipsis and str!']
        err_msg = ('Cannot compare type int of element 1 in tuple '
                   '(1, 2) with limits of types ellipsis and str!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = LimitedTuple(inp, limits=((0, 2), (..., 'b')))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_element_of_named_tuple_uncomparable_upper_bound(self):
        inp = (1, 2)
        log_msg = ['ERROR:root:Cannot compare type int of element 1 '
                   'in tuple test with limits of types ellipsis and str!']
        err_msg = ('Cannot compare type int of element 1 in tuple'
                   ' test with limits of types ellipsis and str!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = LimitedTuple(inp, 'test', limits=((0, 2), (..., 'b')))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)


class TestLimitedTupleMethods(ut.TestCase):

    def test_has_attribute_o(self):
        self.assertTrue(hasattr(LimitedTuple, 'o'))

    def test_attribute_o_is_callable(self):
        self.assertTrue(callable(LimitedTuple.o))

    def test_o_returns_composition(self):
        def f(x):
            return x
        composition = LimitedTuple.o(f)
        self.assertIsInstance(composition, CompositionOf)

    def test_o_raises_error_on_argument_not_callable(self):
        err_msg = ('foo must be a callable that accepts (i) a value,'
                   ' (ii) an optional name for that value, and (iii)'
                   ' any number of keyword arguments!')
        with self.assertRaises(CallableError) as err:
            _ = LimitedTuple.o('foo')
        self.assertEqual(str(err.exception), err_msg)

    def test_has_all_comparable_type_checker_attributes(self):
        all_comparables = (c for c in _ALL_COMPARABLES if c is not TypedDict)
        for comparable in all_comparables:
            self.assertTrue(hasattr(LimitedTuple, comparable.__name__))

    def test_all_comparable_type_checkers_are_type_CompositionOf(self):
        all_comparables = (c for c in _ALL_COMPARABLES if c is not TypedDict)
        for comparable in all_comparables:
            type_checker = getattr(LimitedTuple, comparable.__name__)
            self.assertIsInstance(type_checker, CompositionOf)

    def test_limits_are_passed_through_type_checkers(self):
        inp = (1, 2)
        log_msg = ['ERROR:root:Value 2 of element 1 in tuple test'
                   ' lies outside the allowed interval [3, 5]!']
        err_msg = ('Value 2 of element 1 in tuple test lies'
                   ' outside the allowed interval [3, 5]!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LimitError) as err:
                _ = LimitedTuple.AllInt(inp, 'test', limits=((0, 2), (3, 5)))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)


if __name__ == '__main__':
    ut.main()
