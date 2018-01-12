import logging
import unittest as ut
from ....validators.all import AllNonEmpty
from ....exceptions import IterError, EmptyError, CallableError
from ....types.one import _ITERABLES
from ....types.all import _ALL_ITERABLES
from ....functional import CompositionOf


class TestAllNonEmpty(ut.TestCase):

    def test_error_on_unnamed_variable_not_iterable(self):
        log_msg = ['ERROR:root:Variable 1 with type int does not seem'
                   ' to be an iterable with elements to inspect!']
        err_msg = ('Variable 1 with type int does not seem to'
                   ' be an iterable with elements to inspect!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(IterError) as err:
                _ = AllNonEmpty(1)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_variable_not_iterable(self):
        log_msg = ['ERROR:root:Variable test with type int does not '
                   'seem to be an iterable with elements to inspect!']
        err_msg = ('Variable test with type int does not seem '
                   'to be an iterable with elements to inspect!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(IterError) as err:
                _ = AllNonEmpty(1, 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_sane_tuple(self):
        inputs = ('f', 'o', 'o')
        output = AllNonEmpty(inputs)
        self.assertTupleEqual(output, inputs)

    def test_error_on_empty_element_in_unnamed_tuple(self):
        log_msg = ['ERROR:root:Str must not be empty!',
                   "ERROR:root:An element of the "
                   "tuple ('f', 'o', '') is empty!"]
        err_msg = "An element of the tuple ('f', 'o', '') is empty!"
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(EmptyError) as err:
                _ = AllNonEmpty(('f', 'o', ''))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_empty_element_in_named_tuple(self):
        log_msg = ['ERROR:root:Str must not be empty!',
                   "ERROR:root:An element of the tuple test is empty!"]
        err_msg = "An element of the tuple test is empty!"
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(EmptyError) as err:
                _ = AllNonEmpty(('f', 'o', ''), 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_sane_list(self):
        inputs = ['f', 'o', 'o']
        output = AllNonEmpty(inputs)
        self.assertListEqual(output, inputs)

    def test_error_on_empty_element_in_unnamed_list(self):
        log_msg = ['ERROR:root:Str must not be empty!',
                   "ERROR:root:An element of the "
                   "list ['f', 'o', ''] is empty!"]
        err_msg = "An element of the list ['f', 'o', ''] is empty!"
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(EmptyError) as err:
                _ = AllNonEmpty(['f', 'o', ''])
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_empty_element_in_named_list(self):
        log_msg = ['ERROR:root:Str must not be empty!',
                   "ERROR:root:An element of the list test is empty!"]
        err_msg = "An element of the list test is empty!"
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(EmptyError) as err:
                _ = AllNonEmpty(['f', 'o', ''], 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_sane_set(self):
        inputs = {'f', 'o', 'o'}
        output = AllNonEmpty(inputs)
        self.assertSetEqual(output, inputs)

    def test_error_on_empty_element_in_unnamed_set(self):
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(EmptyError) as err:
                _ = AllNonEmpty({'f', 'o', ''})

    def test_error_on_empty_element_in_named_set(self):
        log_msg = ['ERROR:root:Str must not be empty!',
                   "ERROR:root:An element of the set test is empty!"]
        err_msg = "An element of the set test is empty!"
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(EmptyError) as err:
                _ = AllNonEmpty({'f', 'o', ''}, 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_sane_dict(self):
        inputs = {'f': 1, 'o': 2}
        output = AllNonEmpty(inputs)
        self.assertDictEqual(output, inputs)

    def test_error_on_empty_element_in_unnamed_dict(self):
        log_msg = ['ERROR:root:Str must not be empty!',
                   "ERROR:root:An element of the dict "
                   "{'f': 1, 'o': 2, '': 3} is empty!"]
        err_msg = "An element of the dict {'f': 1, 'o': 2, '': 3} is empty!"
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(EmptyError) as err:
                _ = AllNonEmpty({'f': 1, 'o': 2, '': 3})
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_empty_element_in_named_dict(self):
        log_msg = ['ERROR:root:Str must not be empty!',
                   "ERROR:root:An element of the dict test is empty!"]
        err_msg = "An element of the dict test is empty!"
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(EmptyError) as err:
                _ = AllNonEmpty({'f': 1, 'o': 2, '': 3}, 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_has_iterable_type_checker_attributes(self):
        for iterable in _ITERABLES:
            self.assertTrue(hasattr(AllNonEmpty, iterable.__name__))

    def test_iterable_type_checkers_are_type_CompositionOf(self):
        for iterable in _ITERABLES:
            type_checker = getattr(AllNonEmpty, iterable.__name__)
            self.assertIsInstance(type_checker, CompositionOf)

    def test_has_attribute_NonEmpty(self):
        self.assertTrue(hasattr(AllNonEmpty, 'NonEmpty'))

    def test_attribute_NonEmpty_is_type_CompositionOf(self):
        self.assertIsInstance(AllNonEmpty.NonEmpty, CompositionOf)

    def test_has_all_iterable_type_checker_attributes(self):
        for iterable in _ALL_ITERABLES:
            self.assertTrue(hasattr(AllNonEmpty, iterable.__name__))

    def test_all_iterable_type_checkers_are_type_CompositionOf(self):
        for iterable in _ALL_ITERABLES:
            type_checker = getattr(AllNonEmpty, iterable.__name__)
            self.assertIsInstance(type_checker, CompositionOf)

    def test_works_through_type_and_non_empty_checker(self):
        log_msg = ['ERROR:root:Str must not be empty!',
                   "ERROR:root:An element of the tuple test is empty!"]
        err_msg = "An element of the tuple test is empty!"
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(EmptyError) as err:
                _ = AllNonEmpty.AllStr.NonEmpty(('f', 'o', ''), 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_has_attribute_o(self):
        self.assertTrue(hasattr(AllNonEmpty, 'o'))

    def test_attribute_o_is_callable(self):
        self.assertTrue(callable(AllNonEmpty.o))

    def test_o_returns_composition(self):
        def f(x):
            return x
        composition = AllNonEmpty.o(f)
        self.assertIsInstance(composition, CompositionOf)

    def test_o_raises_error_on_argument_not_callable(self):
        err_msg = ('foo must be a callable that accepts (i) a value,'
                   ' (ii) an optional name for that value, and (iii)'
                   ' any number of keyword arguments!')
        with self.assertRaises(CallableError) as err:
            _ = AllNonEmpty.o('foo')
        self.assertEqual(str(err.exception), err_msg)


if __name__ == '__main__':
    ut.main()
