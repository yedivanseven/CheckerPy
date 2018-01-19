import logging
import unittest as ut
from ....validators.all import AllLimited
from ....exceptions import LimitError, IterError, CallableError
from ....types.one import _ITERABLES
from ....types.all import _ALL_COMPARABLES
from ....functional import CompositionOf


class TestAllLimited(ut.TestCase):

    def test_error_on_unnamed_variable_not_iterable(self):
        log_msg = ['ERROR:root:Variable 1 with type int does not seem'
                   ' to be an iterable with elements to inspect!']
        err_msg = ('Variable 1 with type int does not seem to'
                   ' be an iterable with elements to inspect!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(IterError) as err:
                _ = AllLimited(1)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_variable_not_iterable(self):
        log_msg = ['ERROR:root:Variable test with type int does not '
                   'seem to be an iterable with elements to inspect!']
        err_msg = ('Variable test with type int does not seem '
                   'to be an iterable with elements to inspect!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(IterError) as err:
                _ = AllLimited(1, 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_sane_str(self):
        inputs = 'abc'
        output = AllLimited(inputs, all_lo='a', all_hi='c')
        self.assertEqual(output, inputs)

    def test_error_on_out_of_bounds_element_in_unnamed_str(self):
        log_msg = ['ERROR:root:Value d of str abd with index 2'
                   ' lies outside the allowed interval [a, c]!']
        err_msg = ('Value d of str abd with index 2 lies'
                   ' outside the allowed interval [a, c]!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LimitError) as err:
                _ = AllLimited('abd', all_lo='a', all_hi='c')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_out_of_bounds_element_in_named_str(self):
        log_msg = ['ERROR:root:Value d of str test with index '
                   '2 lies outside the allowed interval [a, c]!']
        err_msg = ('Value d of str test with index 2 lies'
                   ' outside the allowed interval [a, c]!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LimitError) as err:
                _ = AllLimited('abd', 'test', all_lo='a', all_hi='c')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_sane_tuple(self):
        inputs = (1, 2, 3)
        output = AllLimited(inputs, all_lo=1, all_hi=3)
        self.assertTupleEqual(output, inputs)

    def test_error_on_out_of_bounds_element_in_unnamed_tuple(self):
        log_msg = ['ERROR:root:Value 4 of tuple (1, 2, 4) with index'
                   ' 2 lies outside the allowed interval [1, 3]!']
        err_msg = ('Value 4 of tuple (1, 2, 4) with index 2 lies'
                   ' outside the allowed interval [1, 3]!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LimitError) as err:
                _ = AllLimited((1, 2, 4), all_lo=1, all_hi=3)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_out_of_bounds_element_in_named_tuple(self):
        log_msg = ['ERROR:root:Value 4 of tuple test with index '
                   '2 lies outside the allowed interval [1, 3]!']
        err_msg = ('Value 4 of tuple test with index 2 lies'
                   ' outside the allowed interval [1, 3]!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LimitError) as err:
                _ = AllLimited((1, 2, 4), 'test', all_lo=1, all_hi=3)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_sane_list(self):
        inputs = [1, 2, 3]
        output = AllLimited(inputs, all_lo=1, all_hi=3)
        self.assertListEqual(output, inputs)

    def test_error_on_out_of_bounds_element_in_unnamed_list(self):
        log_msg = ['ERROR:root:Value 4 of list [1, 2, 4] with index'
                   ' 2 lies outside the allowed interval [1, 3]!']
        err_msg = ('Value 4 of list [1, 2, 4] with index 2 lies'
                   ' outside the allowed interval [1, 3]!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LimitError) as err:
                _ = AllLimited([1, 2, 4], all_lo=1, all_hi=3)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_out_of_bounds_element_in_named_list(self):
        log_msg = ['ERROR:root:Value 4 of list test with index '
                   '2 lies outside the allowed interval [1, 3]!']
        err_msg = ('Value 4 of list test with index 2 lies'
                   ' outside the allowed interval [1, 3]!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LimitError) as err:
                _ = AllLimited([1, 2, 4], 'test', all_lo=1, all_hi=3)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_sane_set(self):
        inputs = {1, 2, 3}
        output = AllLimited(inputs, all_lo=1, all_hi=3)
        self.assertSetEqual(output, inputs)

    def test_error_on_out_of_bounds_element_in_unnamed_set(self):
        with self.assertLogs(level=logging.ERROR):
            with self.assertRaises(LimitError):
                _ = AllLimited({1, 2, 4}, all_lo=1, all_hi=3)

    def test_error_on_out_of_bounds_element_in_named_set(self):
        log_msg = ['ERROR:root:Value 4 of set test lies '
                   'outside the allowed interval [1, 3]!']
        err_msg = ('Value 4 of set test lies outside'
                   ' the allowed interval [1, 3]!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LimitError) as err:
                _ = AllLimited({1, 2, 4}, 'test', all_lo=1, all_hi=3)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_sane_dict(self):
        inputs = {1: 'one', 2: 'two', 3: 'three'}
        output = AllLimited(inputs, all_lo=1, all_hi=3)
        self.assertDictEqual(output, inputs)

    def test_error_on_out_of_bounds_element_in_unnamed_dict(self):
        inputs = {1: 'one', 2: 'two', 4: 'four'}
        log_msg = ["ERROR:root:Value 4 of dict key in {1: 'one', 2: 'two',"
                   " 4: 'four'} lies outside the allowed interval [1, 3]!"]
        err_msg = ("Value 4 of dict key in {1: 'one', 2: 'two', 4: "
                   "'four'} lies outside the allowed interval [1, 3]!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LimitError) as err:
                _ = AllLimited(inputs, all_lo=1, all_hi=3)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_out_of_bounds_element_in_named_dict(self):
        inputs = {1: 'one', 2: 'two', 4: 'four'}
        log_msg = ['ERROR:root:Value 4 of dict key in test lies'
                   ' outside the allowed interval (-inf, 3]!']
        err_msg = ('Value 4 of dict key in test lies outside'
                   ' the allowed interval (-inf, 3]!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LimitError) as err:
                _ = AllLimited(inputs, 'test', all_hi=3)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_sane_dict_keys(self):
        inputs = {1: 'one', 2: 'two', 3: 'three'}
        output = AllLimited(inputs.keys(), all_lo=1, all_hi=3)
        self.assertSetEqual(set(output), set(inputs.keys()))

    def test_error_on_out_of_bounds_element_in_unnamed_dict_keys(self):
        inputs = {1: 'one', 2: 'two', 4: 'three'}
        log_msg = ['ERROR:root:Value 4 of dict_keys([1, 2, 4]) '
                   'lies outside the allowed interval [1, 3]!']
        err_msg = ('Value 4 of dict_keys([1, 2, 4]) lies '
                   'outside the allowed interval [1, 3]!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LimitError) as err:
                _ = AllLimited(inputs.keys(), all_lo=1, all_hi=3)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_out_of_bounds_element_in_named_dict_keys(self):
        inputs = {1: 'one', 2: 'two', 4: 'three'}
        log_msg = ['ERROR:root:Value 4 of key in dict test lies'
                   ' outside the allowed interval (-inf, 3]!']
        err_msg = ('Value 4 of key in dict test lies outside'
                   ' the allowed interval (-inf, 3]!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LimitError) as err:
                _ = AllLimited(inputs.keys(), 'test', all_hi=3)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_sane_dict_values(self):
        inputs = {'one': 1, 'two': 2, 'three': 3}
        output = AllLimited(inputs.values(), all_lo=1, all_hi=3)
        self.assertSetEqual(set(output), set(inputs.values()))

    def test_error_on_out_of_bounds_element_in_unnamed_dict_values(self):
        inputs = {'one': 1, 'two': 2, 'three': 4}
        log_msg = ['ERROR:root:Value 4 of dict_values([1, 2, 4]) '
                   'lies outside the allowed interval [1, 3]!']
        err_msg = ('Value 4 of dict_values([1, 2, 4]) lies '
                   'outside the allowed interval [1, 3]!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LimitError) as err:
                _ = AllLimited(inputs.values(), all_lo=1, all_hi=3)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_out_of_bounds_element_in_named_dict_values(self):
        inputs = {'one': 1, 'two': 2, 'three': 4}
        log_msg = ['ERROR:root:Value 4 of dict values in test '
                   'lies outside the allowed interval (-inf, 3]!']
        err_msg = ('Value 4 of dict values in test lies '
                   'outside the allowed interval (-inf, 3]!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LimitError) as err:
                _ = AllLimited(inputs.values(), 'test', all_hi=3)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_has_iterable_type_checker_attributes(self):
        for iterable in _ITERABLES:
            self.assertTrue(hasattr(AllLimited, iterable.__name__))

    def test_iterable_type_checkers_are_type_CompositionOf(self):
        for iterable in _ITERABLES:
            type_checker = getattr(AllLimited, iterable.__name__)
            self.assertIsInstance(type_checker, CompositionOf)

    def test_has_attribute_NonEmpty(self):
        self.assertTrue(hasattr(AllLimited, 'NonEmpty'))

    def test_attribute_NonEmpty_is_type_CompositionOf(self):
        self.assertIsInstance(AllLimited.NonEmpty, CompositionOf)

    def test_all_hi_and_lo_are_passed_through_type_and_non_empty_checker(self):
        log_msg = ['ERROR:root:Value d of str test with index 2'
                   ' lies outside the allowed interval (-inf, c]!']
        err_msg = ('Value d of str test with index 2 lies'
                   ' outside the allowed interval (-inf, c]!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LimitError) as err:
                _ = AllLimited.AllStr.NonEmpty('abd', 'test', all_hi='c')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_has_all_comparable_type_checker_attributes(self):
        for iterable in _ALL_COMPARABLES:
            self.assertTrue(hasattr(AllLimited, iterable.__name__))

    def test_all_comparable_type_checkers_are_type_CompositionOf(self):
        for iterable in _ALL_COMPARABLES:
            type_checker = getattr(AllLimited, iterable.__name__)
            self.assertIsInstance(type_checker, CompositionOf)

    def test_has_attribute_o(self):
        self.assertTrue(hasattr(AllLimited, 'o'))

    def test_attribute_o_is_callable(self):
        self.assertTrue(callable(AllLimited.o))

    def test_o_returns_composition(self):
        def f(x):
            return x
        composition = AllLimited.o(f)
        self.assertIsInstance(composition, CompositionOf)

    def test_o_raises_error_on_argument_not_callable(self):
        err_msg = ('foo must be a callable that accepts (i) a value,'
                   ' (ii) an optional name for that value, and (iii)'
                   ' any number of keyword arguments!')
        with self.assertRaises(CallableError) as err:
            _ = AllLimited.o('foo')
        self.assertEqual(str(err.exception), err_msg)


if __name__ == '__main__':
    ut.main()
