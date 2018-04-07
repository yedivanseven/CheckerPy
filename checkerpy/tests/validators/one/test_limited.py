import logging
import unittest as ut
from collections import defaultdict, deque, OrderedDict
from ....validators.one import Limited
from ....exceptions import WrongTypeError, LimitError, CallableError
from ....types.one import _COMPARABLES
from ....types.weak import _LIKE_COMPARABLES
from ....functional import CompositionOf


class TestLimitedWorks(ut.TestCase):

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

    def test_works_with_sane_deque(self):
        out = Limited(deque([2, 3]), lo=deque([1, 2]), hi=deque([3, 4]))
        self.assertIsInstance(out, deque)
        self.assertEqual(out, deque([2, 3]))

    def test_works_with_sane_set(self):
        out = Limited({2, 3}, lo={1, 2}, hi={3, 4})
        self.assertIsInstance(out, set)
        self.assertSetEqual(out, {2, 3})

    def test_works_with_sane_frozenset(self):
        inp = frozenset({2, 3})
        out = Limited(inp, lo=frozenset({1}), hi=frozenset({4, 5, 6}))
        self.assertIsInstance(out, type(inp))
        self.assertSetEqual(out, inp)

    def test_works_with_sane_dict_keys(self):
        inp = {2: 'two'}.keys()
        out = Limited(inp, lo={1: 'one'}.keys(), hi={3: 'three'}.keys())
        self.assertIsInstance(out, type(inp))
        self.assertEqual(out, inp)

    def test_works_with_sane_dict_items(self):
        inp = {2: 'bbb'}.items()
        out = Limited(inp, lo={1: 'aaa'}.items(), hi={3: 'ccc'}.items())
        self.assertIsInstance(out, type(inp))
        self.assertEqual(out, inp)

    def test_works_with_sane_ordered_dict_keys(self):
        inp = OrderedDict({2: 'two'}).keys()
        lo = OrderedDict({2: 'two'})
        hi = OrderedDict({2: 'two'})
        out = Limited(inp, lo=lo.keys(), hi=hi.keys())
        self.assertIsInstance(out, type(inp))
        self.assertEqual(out, inp)

    def test_works_with_sane_ordered_dict_items(self):
        inp = OrderedDict({2: 'bbb'}).items()
        lo = OrderedDict({1: 'aaa'})
        hi = OrderedDict({3: 'ccc'})
        out = Limited(inp, lo=lo.items(), hi=hi.items())
        self.assertIsInstance(out, type(inp))
        self.assertEqual(out, inp)

    def test_works_with_sane_defaultdict_keys(self):
        inp = defaultdict(str, {2: 'two'}).keys()
        lo = defaultdict(str, {2: 'two'})
        hi = defaultdict(str, {2: 'two'})
        out = Limited(inp, lo=lo.keys(), hi=hi.keys())
        self.assertIsInstance(out, type(inp))
        self.assertEqual(out, inp)

    def test_works_with_sane_defaultdict_items(self):
        inp = defaultdict(str, {2: 'bbb'}).items()
        lo = defaultdict(str, {1: 'aaa'})
        hi = defaultdict(str, {3: 'ccc'})
        out = Limited(inp, lo=lo.items(), hi=hi.items())
        self.assertIsInstance(out, type(inp))
        self.assertEqual(out, inp)


class TestLimitedUncomparable(ut.TestCase):

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

    def test_error_on_unnamed_deque_uncomparable(self):
        inp = deque([1])
        log_msg = ['ERROR:root:Cannot compare deque([1])'
                   ' with limits of types float and int!']
        err_msg = ('Cannot compare deque([1])'
                   ' with limits of types float and int!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = Limited(inp, lo=1.0, hi=2)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_deque_uncomparable(self):
        inp = deque([1])
        log_msg = ['ERROR:root:Cannot compare type deque'
                   ' of test with limits of types float and int!']
        err_msg = ('Cannot compare type deque'
                   ' of test with limits of types float and int!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = Limited(inp, 'test', lo=1.0, hi=2)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_unnamed_frozenset_uncomparable(self):
        inp = frozenset({1})
        log_msg = ['ERROR:root:Cannot compare frozenset({1})'
                   ' with limits of types float and int!']
        err_msg = ('Cannot compare frozenset({1})'
                   ' with limits of types float and int!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = Limited(inp, lo=1.0, hi=2)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_frozenset_uncomparable(self):
        inp = frozenset({1})
        log_msg = ['ERROR:root:Cannot compare type frozenset'
                   ' of test with limits of types float and int!']
        err_msg = ('Cannot compare type frozenset'
                   ' of test with limits of types float and int!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = Limited(inp, 'test', lo=1.0, hi=2)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_unnamed_ordered_dict_uncomparable(self):
        inp = OrderedDict({1: 1})
        log_msg = ['ERROR:root:Cannot compare OrderedDict([(1, 1)])'
                   ' with limits of types float and int!']
        err_msg = ('Cannot compare OrderedDict([(1, 1)])'
                   ' with limits of types float and int!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = Limited(inp, lo=1.0, hi=2)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_ordered_dict_uncomparable(self):
        inp = OrderedDict({1: 1})
        log_msg = ['ERROR:root:Cannot compare type OrderedDict'
                   ' of test with limits of types float and int!']
        err_msg = ('Cannot compare type OrderedDict'
                   ' of test with limits of types float and int!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = Limited(inp, 'test', lo=1.0, hi=2)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_unnamed_defaultdict_uncomparable(self):
        inp = defaultdict(int, {1: 1})
        log_msg = ["ERROR:root:Cannot compare defaultdict(<class 'int'>,"
                   " {1: 1}) with limits of types float and int!"]
        err_msg = ("Cannot compare defaultdict(<class 'int'>, {1: 1})"
                   " with limits of types float and int!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = Limited(inp, lo=1.0, hi=2)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_defaultdict_uncomparable(self):
        inp = defaultdict(int, {1: 1})
        log_msg = ['ERROR:root:Cannot compare type defaultdict'
                   ' of test with limits of types float and int!']
        err_msg = ('Cannot compare type defaultdict'
                   ' of test with limits of types float and int!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = Limited(inp, 'test', lo=1.0, hi=2)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_unnamed_dict_keys_uncomparable(self):
        inp = {1: 1}
        log_msg = ['ERROR:root:Cannot compare dict_keys([1])'
                   ' with limits of types float and int!']
        err_msg = ('Cannot compare dict_keys([1])'
                   ' with limits of types float and int!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = Limited(inp.keys(), lo=1.0, hi=2)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_dict_keys_uncomparable(self):
        inp = {1: 1}
        log_msg = ['ERROR:root:Cannot compare type dict_keys'
                   ' of test with limits of types float and int!']
        err_msg = ('Cannot compare type dict_keys'
                   ' of test with limits of types float and int!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = Limited(inp.keys(), 'test', lo=1.0, hi=2)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_unnamed_ordered_dict_keys_uncomparable(self):
        inp = OrderedDict({1: 1})
        log_msg = ['ERROR:root:Cannot compare odict_keys([1])'
                   ' with limits of types float and int!']
        err_msg = ('Cannot compare odict_keys([1])'
                   ' with limits of types float and int!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = Limited(inp.keys(), lo=1.0, hi=2)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_ordered_dict_keys_uncomparable(self):
        inp = OrderedDict({1: 1})
        log_msg = ['ERROR:root:Cannot compare type odict_keys'
                   ' of test with limits of types float and int!']
        err_msg = ('Cannot compare type odict_keys'
                   ' of test with limits of types float and int!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = Limited(inp.keys(), 'test', lo=1.0, hi=2)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_unnamed_dict_values_uncomparable(self):
        inp = {1: 1}
        log_msg = ['ERROR:root:Cannot compare dict_values([1])'
                   ' with limits of types float and int!']
        err_msg = ('Cannot compare dict_values([1])'
                   ' with limits of types float and int!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = Limited(inp.values(), lo=1.0, hi=2)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_dict_values_uncomparable(self):
        inp = {1: 1}
        log_msg = ['ERROR:root:Cannot compare type dict_values'
                   ' of test with limits of types float and int!']
        err_msg = ('Cannot compare type dict_values'
                   ' of test with limits of types float and int!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = Limited(inp.values(), 'test', lo=1.0, hi=2)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_unnamed_ordered_dict_values_uncomparable(self):
        inp = OrderedDict({1: 1})
        log_msg = ['ERROR:root:Cannot compare odict_values([1])'
                   ' with limits of types float and int!']
        err_msg = ('Cannot compare odict_values([1])'
                   ' with limits of types float and int!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = Limited(inp.values(), lo=1.0, hi=2)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_ordered_dict_values_uncomparable(self):
        inp = OrderedDict({1: 1})
        log_msg = ['ERROR:root:Cannot compare type odict_values'
                   ' of test with limits of types float and int!']
        err_msg = ('Cannot compare type odict_values'
                   ' of test with limits of types float and int!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = Limited(inp.values(), 'test', lo=1.0, hi=2)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_unnamed_dict_items_uncomparable(self):
        inp = {1: 1}
        log_msg = ['ERROR:root:Cannot compare dict_items([(1, 1)])'
                   ' with limits of types float and int!']
        err_msg = ('Cannot compare dict_items([(1, 1)])'
                   ' with limits of types float and int!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = Limited(inp.items(), lo=1.0, hi=2)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_dict_items_uncomparable(self):
        inp = {1: 1}
        log_msg = ['ERROR:root:Cannot compare type dict_items'
                   ' of test with limits of types float and int!']
        err_msg = ('Cannot compare type dict_items'
                   ' of test with limits of types float and int!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = Limited(inp.items(), 'test', lo=1.0, hi=2)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_unnamed_ordered_dict_items_uncomparable(self):
        inp = OrderedDict({1: 1})
        log_msg = ['ERROR:root:Cannot compare odict_items([(1, 1)])'
                   ' with limits of types float and int!']
        err_msg = ('Cannot compare odict_items([(1, 1)])'
                   ' with limits of types float and int!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = Limited(inp.items(), lo=1.0, hi=2)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_ordered_dict_items_uncomparable(self):
        inp = OrderedDict({1: 1})
        log_msg = ['ERROR:root:Cannot compare type odict_items'
                   ' of test with limits of types float and int!']
        err_msg = ('Cannot compare type odict_items'
                   ' of test with limits of types float and int!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = Limited(inp.items(), 'test', lo=1.0, hi=2)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)


class TestLimitedOutOfBounds(ut.TestCase):

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


class TestLimitedMethods(ut.TestCase):

    def test_has_comparable_type_checker_attributes(self):
        for comparable in _COMPARABLES:
            self.assertTrue(hasattr(Limited, comparable.__name__))
        for comparable in _LIKE_COMPARABLES:
            self.assertTrue(hasattr(Limited, comparable.__name__))

    def test_comparable_type_checkers_are_type_CompositionOf(self):
        for comparable in _COMPARABLES:
            type_checker = getattr(Limited, comparable.__name__)
            self.assertIsInstance(type_checker, CompositionOf)
        for comparable in _LIKE_COMPARABLES:
            type_checker = getattr(Limited, comparable.__name__)
            self.assertIsInstance(type_checker, CompositionOf)

    def test_has_attribute_NonEmpty(self):
        self.assertTrue(hasattr(Limited, 'NonEmpty'))

    def test_attribute_NonEmpty_is_type_CompositionOf(self):
        self.assertIsInstance(Limited.NonEmpty, CompositionOf)

    def test_has_attribute_JustLen(self):
        self.assertTrue(hasattr(Limited, 'JustLen'))

    def test_attribute_JustLen_is_type_CompositionOf(self):
        self.assertIsInstance(Limited.JustLen, CompositionOf)

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
