import logging
import unittest as ut
from ....validators.all import AllLen
from ....exceptions import LenError, IterError, CallableError
from ....types.one import _ITERABLES
from ....types.all import _ALL_ITERABLES
from ....functional import CompositionOf


class TestAllLen(ut.TestCase):

    def test_error_on_unnamed_variable_not_iterable(self):
        log_msg = ['ERROR:root:Variable 1 with type int does not seem'
                   ' to be an iterable with elements to inspect!']
        err_msg = ('Variable 1 with type int does not seem to'
                   ' be an iterable with elements to inspect!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(IterError) as err:
                _ = AllLen(1)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_variable_not_iterable(self):
        log_msg = ['ERROR:root:Variable test with type int does not '
                   'seem to be an iterable with elements to inspect!']
        err_msg = ('Variable test with type int does not seem '
                   'to be an iterable with elements to inspect!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(IterError) as err:
                _ = AllLen(1, 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_sane_tuple(self):
        inputs = ('foo', 'bar', 'baz')
        output = AllLen(inputs, length=3)
        self.assertTupleEqual(output, inputs)

    def test_error_on_empty_element_in_unnamed_tuple(self):
        log_msg = ['ERROR:root:Length of str ba must be 3, not 2!',
                   "ERROR:root:An element of the tuple "
                   "('foo', 'ba', 'baz') has the wrong length!"]
        err_msg = ("An element of the tuple ('foo', 'ba',"
                   " 'baz') has the wrong length!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = AllLen(('foo', 'ba', 'baz'), length=3)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_empty_element_in_named_tuple(self):
        log_msg = ['ERROR:root:Length of str ba must be 3, not 2!',
                   "ERROR:root:An element of the tuple"
                   " test has the wrong length!"]
        err_msg = "An element of the tuple test has the wrong length!"
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = AllLen(('foo', 'ba', 'baz'), 'test', length=3)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_sane_list(self):
        inputs = ['foo', 'bar', 'baz']
        output = AllLen(inputs, length=3)
        self.assertListEqual(output, inputs)

    def test_error_on_empty_element_in_unnamed_list(self):
        log_msg = ['ERROR:root:Length of str ba must be 3, not 2!',
                   "ERROR:root:An element of the list ['foo',"
                   " 'ba', 'baz'] has the wrong length!"]
        err_msg = ("An element of the list ['foo', 'ba',"
                   " 'baz'] has the wrong length!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = AllLen(['foo', 'ba', 'baz'], length=3)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_empty_element_in_named_list(self):
        log_msg = ['ERROR:root:Length of str ba must be 3, not 2!',
                   "ERROR:root:An element of the list"
                   " test has the wrong length!"]
        err_msg = "An element of the list test has the wrong length!"
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = AllLen(['foo', 'ba', 'baz'], 'test', length=3)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_sane_set(self):
        inputs = {'foo', 'bar', 'baz'}
        output = AllLen(inputs, length=3)
        self.assertSetEqual(output, inputs)

    def test_error_on_empty_element_in_unnamed_set(self):
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = AllLen({'foo', 'ba', 'baz'}, length=3)

    def test_error_on_empty_element_in_named_set(self):
        log_msg = ['ERROR:root:Length of str ba must be 3, not 2!',
                   "ERROR:root:An element of the set"
                   " test has the wrong length!"]
        err_msg = "An element of the set test has the wrong length!"
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = AllLen({'foo', 'ba', 'baz'}, 'test', length=3)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_sane_dict(self):
        inputs = {'foo': 1, 'bar': 2, 'baz': 3}
        output = AllLen(inputs, length=3)
        self.assertDictEqual(output, inputs)

    def test_error_on_empty_element_in_unnamed_dict(self):
        log_msg = ['ERROR:root:Length of str ba must be 3, not 2!',
                   "ERROR:root:An element of the dict {'foo': 1,"
                   " 'ba': 2, 'baz': 3} has the wrong length!"]
        err_msg = ("An element of the dict {'foo': 1, 'ba': 2,"
                   " 'baz': 3} has the wrong length!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = AllLen({'foo': 1, 'ba': 2, 'baz': 3}, length=3)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_empty_element_in_named_dict(self):
        log_msg = ['ERROR:root:Length of str ba must be 3, not 2!',
                   "ERROR:root:An element of the dict"
                   " test has the wrong length!"]
        err_msg = "An element of the dict test has the wrong length!"
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = AllLen({'foo': 1, 'ba': 2, 'baz': 3}, 'test', length=3)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_has_iterable_type_checker_attributes(self):
        for iterable in _ITERABLES:
            self.assertTrue(hasattr(AllLen, iterable.__name__))

    def test_iterable_type_checkers_are_type_CompositionOf(self):
        for iterable in _ITERABLES:
            type_checker = getattr(AllLen, iterable.__name__)
            self.assertIsInstance(type_checker, CompositionOf)

    def test_has_attribute_NonEmpty(self):
        self.assertTrue(hasattr(AllLen, 'NonEmpty'))

    def test_attribute_NonEmpty_is_type_CompositionOf(self):
        self.assertIsInstance(AllLen.NonEmpty, CompositionOf)

    def test_has_all_iterable_type_checker_attributes(self):
        for iterable in _ALL_ITERABLES:
            self.assertTrue(hasattr(AllLen, iterable.__name__))

    def test_all_iterable_type_checkers_are_type_CompositionOf(self):
        for iterable in _ALL_ITERABLES:
            type_checker = getattr(AllLen, iterable.__name__)
            self.assertIsInstance(type_checker, CompositionOf)

    def test_length_is_passed_through_type_checker(self):
        log_msg = ['ERROR:root:Length of str ba must be 3, not 2!',
                   "ERROR:root:An element of the tuple"
                   " test has the wrong length!"]
        err_msg = "An element of the tuple test has the wrong length!"
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = AllLen.AllStr(('foo', 'ba', 'baz'), 'test', length=3)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_has_attribute_o(self):
        self.assertTrue(hasattr(AllLen, 'o'))

    def test_attribute_o_is_callable(self):
        self.assertTrue(callable(AllLen.o))

    def test_o_returns_composition(self):
        def f(x):
            return x
        composition = AllLen.o(f)
        self.assertIsInstance(composition, CompositionOf)

    def test_o_raises_error_on_argument_not_callable(self):
        err_msg = ('foo must be a callable that accepts (i) a value,'
                   ' (ii) an optional name for that value, and (iii)'
                   ' any number of keyword arguments!')
        with self.assertRaises(CallableError) as err:
            _ = AllLen.o('foo')
        self.assertEqual(str(err.exception), err_msg)


if __name__ == '__main__':
    ut.main()
