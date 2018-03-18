import logging
import unittest as ut
from ....validators.one import JustLen
from ....exceptions import LenError, IntError, CallableError
from ....types.one import _ITERABLES
from ....functional import CompositionOf


class TestJustLen(ut.TestCase):

    def test_error_on_one_length_not_convertible_to_int(self):
        err_msg = ('Could not convert given length f '
                   'of type str to required type int!')
        with self.assertRaises(IntError) as err:
            _ = JustLen([1, 2], length='foo')
        self.assertEqual(str(err.exception), err_msg)

    def test_error_on_one_of_two_lengths_not_convertible_to_int(self):
        err_msg = ('Could not convert given length bar'
                   ' of type str to required type int!')
        with self.assertRaises(IntError) as err:
            _ = JustLen([1, 2], length=(3, 'bar'))
        self.assertEqual(str(err.exception), err_msg)

    def test_error_on_invalid_unnamed_argument(self):
        log_msg = ['ERROR:root:Length of 1 with '
                   'type int cannot be determined!']
        err_msg = 'Length of 1 with type int cannot be determined!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = JustLen(1, length=4)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_invalid_named_argument(self):
        log_msg = ['ERROR:root:Length of test with '
                   'type int cannot be determined!']
        err_msg = 'Length of test with type int cannot be determined!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = JustLen(2, 'test', length=4)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_sane_str(self):
        out = JustLen('test', length=4)
        self.assertIsInstance(out, str)
        self.assertEqual(out, 'test')

    def test_error_on_length_of_str_not_in_lengths(self):
        log_msg = ['ERROR:root:Length of str foo '
                   'must be one of (4, 5), not 3!']
        err_msg = 'Length of str foo must be one of (4, 5), not 3!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = JustLen('foo', length=(4, 5))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_unnamed_str_wrong_length(self):
        log_msg = ['ERROR:root:Length of str bar must be 6, not 3!']
        err_msg = 'Length of str bar must be 6, not 3!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = JustLen('bar', length=6)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_str_wrong_length(self):
        log_msg = ['ERROR:root:Length of str test must be 7, not 3!']
        err_msg = 'Length of str test must be 7, not 3!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = JustLen('baz', 'test', length=7)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_sane_tuple(self):
        out = JustLen((1, 2), length=2)
        self.assertIsInstance(out, tuple)
        self.assertEqual(out, (1, 2))

    def test_error_on_length_of_tuple_not_in_lengths(self):
        log_msg = ['ERROR:root:Length of tuple (1, 2, 3)'
                   ' must be one of (4, 5), not 3!']
        err_msg = 'Length of tuple (1, 2, 3) must be one of (4, 5), not 3!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = JustLen((1, 2, 3), length=(4, 5))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_unnamed_tuple_wrong_length(self):
        log_msg = ['ERROR:root:Length of tuple (1, 2, 3) must be 6, not 3!']
        err_msg = 'Length of tuple (1, 2, 3) must be 6, not 3!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = JustLen((1, 2, 3), length=6)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_tuple_wrong_length(self):
        log_msg = ['ERROR:root:Length of tuple test must be 7, not 3!']
        err_msg = 'Length of tuple test must be 7, not 3!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = JustLen((1, 2, 3), 'test', length=7)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_sane_list(self):
        out = JustLen([1, 2], length=2)
        self.assertIsInstance(out, list)
        self.assertListEqual(out, [1, 2])

    def test_error_on_length_of_list_not_in_lengths(self):
        log_msg = ['ERROR:root:Length of list [1, 2, 3]'
                   ' must be one of (4, 5), not 3!']
        err_msg = 'Length of list [1, 2, 3] must be one of (4, 5), not 3!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = JustLen([1, 2, 3], length=(4, 5))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_unnamed_list_wrong_length(self):
        log_msg = ['ERROR:root:Length of list [1, 2, 3] must be 6, not 3!']
        err_msg = 'Length of list [1, 2, 3] must be 6, not 3!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = JustLen([1, 2, 3], length=6)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_list_wrong_length(self):
        log_msg = ['ERROR:root:Length of list test must be 7, not 3!']
        err_msg = 'Length of list test must be 7, not 3!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = JustLen([1, 2, 3], 'test', length=7)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_sane_set(self):
        out = JustLen({1, 2}, length=2)
        self.assertIsInstance(out, set)
        self.assertSetEqual(out, {1, 2})

    def test_error_on_length_of_set_not_in_lengths(self):
        log_msg = ['ERROR:root:Length of set {1, 2, 3}'
                   ' must be one of (4, 5), not 3!']
        err_msg = 'Length of set {1, 2, 3} must be one of (4, 5), not 3!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = JustLen({1, 2, 3}, length=(4, 5))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_unnamed_set_wrong_length(self):
        log_msg = ['ERROR:root:Length of set {1, 2, 3} must be 6, not 3!']
        err_msg = 'Length of set {1, 2, 3} must be 6, not 3!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = JustLen({1, 2, 3}, length=6)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_set_wrong_length(self):
        log_msg = ['ERROR:root:Length of set test must be 7, not 3!']
        err_msg = 'Length of set test must be 7, not 3!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = JustLen({1, 2, 3}, 'test', length=7)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_sane_frozenset(self):
        out = JustLen(frozenset((1, 2)), length=2)
        self.assertIsInstance(out, frozenset)
        self.assertSetEqual(out, frozenset((1, 2)))

    def test_error_on_length_of_frozenset_not_in_lengths(self):
        log_msg = ['ERROR:root:Length of frozenset({1, 2, 3})'
                   ' must be one of (4, 5), not 3!']
        err_msg = ('Length of frozenset({1, 2, 3}) '
                   'must be one of (4, 5), not 3!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = JustLen(frozenset({1, 2, 3}), length=(4, 5))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_unnamed_frozenset_wrong_length(self):
        log_msg = ['ERROR:root:Length of frozenset({1, 2, 3})'
                   ' must be 6, not 3!']
        err_msg = 'Length of frozenset({1, 2, 3}) must be 6, not 3!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = JustLen(frozenset({1, 2, 3}), length=6)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_frozenset_wrong_length(self):
        log_msg = ['ERROR:root:Length of frozenset test must be 7, not 3!']
        err_msg = 'Length of frozenset test must be 7, not 3!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = JustLen(frozenset({1, 2, 3}), 'test', length=7)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_sane_dict(self):
        out = JustLen({1: 'one', 2: 'two'}, length=2)
        self.assertIsInstance(out, dict)
        self.assertDictEqual(out, {1: 'one', 2: 'two'})

    def test_error_on_length_of_dict_not_in_lengths(self):
        log_msg = ["ERROR:root:Length of dict {1: 'one', 2: 'two'}"
                   " must be one of (4, 5), not 2!"]
        err_msg = ("Length of dict {1: 'one', 2: 'two'}"
                   " must be one of (4, 5), not 2!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = JustLen({1: 'one', 2: 'two'}, length=(4, 5))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_unnamed_dict_wrong_length(self):
        log_msg = ["ERROR:root:Length of dict {1: 'one', 2: 'two'}"
                   " must be 6, not 2!"]
        err_msg = "Length of dict {1: 'one', 2: 'two'} must be 6, not 2!"
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = JustLen({1: 'one', 2: 'two'}, length=6)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_dict_wrong_length(self):
        log_msg = ['ERROR:root:Length of dict test must be 7, not 2!']
        err_msg = 'Length of dict test must be 7, not 2!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = JustLen({1: 'one', 2: 'two'}, 'test', length=7)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_sane_dict_keys(self):
        inp = {1: 'one', 2: 'two'}
        out = JustLen(inp.keys(), length=2)
        self.assertIsInstance(out, type(inp.keys()))
        self.assertEqual(out, inp.keys())

    def test_error_on_length_of_dict_keys_not_in_lengths(self):
        log_msg = ['ERROR:root:Length of dict_keys([1, 2])'
                   ' must be one of (4, 5), not 2!']
        err_msg = 'Length of dict_keys([1, 2]) must be one of (4, 5), not 2!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = JustLen({1: 'one', 2: 'two'}.keys(), length=(4, 5))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_unnamed_dict_keys_wrong_length(self):
        log_msg = ['ERROR:root:Length of dict_keys([1, 2]) must be 6, not 2!']
        err_msg = 'Length of dict_keys([1, 2]) must be 6, not 2!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = JustLen({1: 'one', 2: 'two'}.keys(), length=6)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_dict_keys_wrong_length(self):
        log_msg = ['ERROR:root:Length of dict_keys test must be 7, not 2!']
        err_msg = 'Length of dict_keys test must be 7, not 2!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = JustLen({1: 'one', 2: 'two'}.keys(), 'test', length=7)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_sane_dict_values(self):
        inp = {1: 'one', 2: 'two'}
        out = JustLen(inp.values(), length=2)
        self.assertIsInstance(out, type(inp.values()))

    def test_error_on_length_of_dict_values_not_in_lengths(self):
        log_msg = ['ERROR:root:Length of dict_values([1, 2])'
                   ' must be one of (4, 5), not 2!']
        err_msg = 'Length of dict_values([1, 2]) must be one of (4, 5), not 2!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = JustLen({'one': 1, 'two': 2}.values(), length=(4, 5))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_unnamed_dict_values_wrong_length(self):
        log_msg = ['ERROR:root:Length of dict_values([1, 2])'
                   ' must be 6, not 2!']
        err_msg = 'Length of dict_values([1, 2]) must be 6, not 2!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = JustLen({'one': 1, 'two': 2}.values(), length=6)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_dict_values_wrong_length(self):
        log_msg = ['ERROR:root:Length of dict_values test must be 7, not 2!']
        err_msg = 'Length of dict_values test must be 7, not 2!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = JustLen({1: 'one', 2: 'two'}.values(), 'test', length=7)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_sane_dict_items(self):
        inp = {1: 'one', 2: 'two'}
        out = JustLen(inp.items(), length=2)
        self.assertIsInstance(out, type(inp.items()))

    def test_error_on_length_of_dict_items_not_in_lengths(self):
        log_msg = ["ERROR:root:Length of dict_items([('one', 1), ('two', 2)])"
                   " must be one of (4, 5), not 2!"]
        err_msg = ("Length of dict_items([('one', 1), ('two', 2)])"
                   " must be one of (4, 5), not 2!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = JustLen({'one': 1, 'two': 2}.items(), length=(4, 5))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_unnamed_dict_items_wrong_length(self):
        log_msg = ["ERROR:root:Length of dict_items([('one', 1), ('two', 2)])"
                   " must be 6, not 2!"]
        err_msg = ("Length of dict_items([('one', 1), ('two', 2)])"
                   " must be 6, not 2!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = JustLen({'one': 1, 'two': 2}.items(), length=6)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_dict_items_wrong_length(self):
        log_msg = ['ERROR:root:Length of dict_items test must be 7, not 2!']
        err_msg = 'Length of dict_items test must be 7, not 2!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = JustLen({1: 'one', 2: 'two'}.items(), 'test', length=7)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_has_iterable_type_checker_attributes(self):
        for iterable in _ITERABLES:
            self.assertTrue(hasattr(JustLen, iterable.__name__))

    def test_iterable_type_checkers_are_type_CompositionOf(self):
        for iterable in _ITERABLES:
            type_checker = getattr(JustLen, iterable.__name__)
            self.assertIsInstance(type_checker, CompositionOf)

    def test_length_is_passed_through_type_checker(self):
        log_msg = ['ERROR:root:Length of str bar must be 6, not 3!']
        err_msg = 'Length of str bar must be 6, not 3!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = JustLen.JustStr('bar', length=6)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_has_attribute_o(self):
        self.assertTrue(hasattr(JustLen, 'o'))

    def test_attribute_o_is_callable(self):
        self.assertTrue(callable(JustLen.o))

    def test_o_returns_composition(self):
        def f(x):
            return x
        composition = JustLen.o(f)
        self.assertIsInstance(composition, CompositionOf)

    def test_o_raises_error_on_argument_not_callable(self):
        err_msg = ('foo must be a callable that accepts (i) a value,'
                   ' (ii) an optional name for that value, and (iii)'
                   ' any number of keyword arguments!')
        with self.assertRaises(CallableError) as err:
            _ = JustLen.o('foo')
        self.assertEqual(str(err.exception), err_msg)


if __name__ == '__main__':
    ut.main()
