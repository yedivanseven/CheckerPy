import logging
import unittest as ut
from ....functional import CompositionOf
from ....types.all import All
from ....types.one import _ITERABLES
from ....exceptions import WrongTypeError, CallableError, IterError


class TestAllInstatiation(ut.TestCase):

    def test_error_on_wrong_identifier(self):
        err_msg = 'Type-checker name @foo is not a valid identifier!'
        with self.assertRaises(ValueError) as err:
            _ = All(int, identifier='@foo')
        self.assertEqual(str(err.exception), err_msg)

    def test_has_default_name(self):
        AllInt = All(int)
        self.assertEqual(AllInt.__name__, 'All')

    def test_identifier_sets_name_attribute(self):
        AllInt = All(int, identifier='AllInt')
        self.assertEqual(AllInt.__name__, 'AllInt')

    def test_has_attribute_types_with_one_valid_type(self):
        AllInt = All(int)
        self.assertTrue(hasattr(AllInt, 'types'))

    def test_cannot_set_attribute_types(self):
        AllInt = All(int)
        with self.assertRaises(AttributeError):
            AllInt.types = 'foo'

    def test_attribute_types_has_correct_value_with_one_valid_type(self):
        AllInt = All(int)
        self.assertTupleEqual(AllInt.types, (int, ))

    def test_works_with_two_valid_types(self):
        _ = All(int, float)

    def test_has_attribute_types_with_two_valid_types(self):
        AllNum = All(int, float)
        self.assertTrue(hasattr(AllNum, 'types'))

    def test_attribute_types_has_correct_value_with_two_valid_types(self):
        AllNum = All(int, float)
        self.assertTupleEqual(AllNum.types, (int, float))


class TestAll(ut.TestCase):

    def test_returns_correct_value_with_str(self):
        AllStr = All(str)
        s = AllStr('foo')
        self.assertEqual(s, 'foo')

    def test_returns_correct_value_with_tuple(self):
        AllStr = All(str)
        t = AllStr(('f', 'o', 'o'))
        self.assertTupleEqual(t, ('f', 'o', 'o'))

    def test_returns_correct_value_with_list(self):
        AllStr =All(str)
        l = AllStr(['f', 'o', 'o'])
        self.assertListEqual(l, ['f', 'o', 'o'])

    def test_returns_correct_value_with_set(self):
        AllStr = All(str)
        s = AllStr({'f', 'o', 'o'})
        self.assertSetEqual(s, {'f', 'o'})

    def test_returns_correct_value_with_dict(self):
        AllStr = All(str)
        d = AllStr({'f': 1, 'o': 2})
        self.assertDictEqual(d, {'f': 1, 'o': 2})

    def test_returns_correct_type_with_two_types(self):
        AllNum = All(int, float)
        i = AllNum((1, ))
        self.assertIsInstance(i, tuple)
        f = AllNum([1.0])
        self.assertIsInstance(f, list)

    def test_returns_correct_value_with_two_types(self):
        AllNum = All(int, float)
        self.assertTupleEqual(AllNum((2, )), (2, ))
        self.assertListEqual(AllNum([2.0]), [2.0])

    def test_error_on_unnamed_variable_not_iterable(self):
        AllInt = All(int)
        log_msg = ['ERROR:root:Variable 3 with type int does not seem'
                   ' to be an iterable with elements to inspect!']
        err_msg = ('Variable 3 with type int does not seem to'
                   ' be an iterable with elements to inspect!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(IterError) as err:
                _ = AllInt(3)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_variable_not_iterable(self):
        AllInt = All(int)
        log_msg = ['ERROR:root:Variable test with type int does not '
                   'seem to be an iterable with elements to inspect!']
        err_msg = ('Variable test with type int does not seem '
                   'to be an iterable with elements to inspect!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(IterError) as err:
                _ = AllInt(3, 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_wrong_unnamed_variable_with_one_type(self):
        AllInt = All(int)
        log_msg = ['ERROR:root:Type of element 1 in tuple (4,'
                   ' 5.0) must be int, not float like 5.0!']
        err_msg = ('Type of element 1 in tuple (4, 5.0)'
                   ' must be int, not float like 5.0!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = AllInt((4, 5.0))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_wrong_unnamed_dict_with_one_type(self):
        AllInt = All(int)
        log_msg = ["ERROR:root:Type of key in dict {4: 'four', "
                   "5.0: 'five'} must be int, not float like 5.0!"]
        err_msg = ("Type of key in dict {4: 'four', 5.0: "
                   "'five'} must be int, not float like 5.0!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = AllInt({4: 'four', 5.0: 'five'})
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_wrong_unnamed_set_with_one_type(self):
        AllInt = All(int)
        log_msg = ["ERROR:root:Type of element in set {4, "
                   "5.0} must be int, not float like 5.0!"]
        err_msg = ("Type of element in set {4, 5.0} must"
                   " be int, not float like 5.0!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = AllInt({4, 5.0})
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_wrong_named_variable_with_one_type(self):
        AllInt = All(int)
        log_msg = ['ERROR:root:Type of element 1 in tuple '
                   'test must be int, not float like 5.0!']
        err_msg = ('Type of element 1 in tuple test '
                   'must be int, not float like 5.0!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = AllInt((4, 5.0), 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_wrong_named_dict_with_one_type(self):
        AllInt = All(int)
        log_msg = ['ERROR:root:Type of key in dict test'
                   ' must be int, not float like 5.0!']
        err_msg = ('Type of key in dict test must'
                   ' be int, not float like 5.0!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = AllInt({4: 'four', 5.0: 'five'}, 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_wrong_named_set_with_one_type(self):
        AllInt = All(int)
        log_msg = ['ERROR:root:Type of element in set test'
                   ' must be int, not float like 5.0!']
        err_msg = ('Type of element in set test must'
                   ' be int, not float like 5.0!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = AllInt({4, 5.0}, 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_wrong_unnamed_variable_with_two_types(self):
        AllNum = All(int, float)
        log_msg = ["ERROR:root:Type of element 2 in tuple (4, 5.0, 'bar')"
                   " must be one of ('int', 'float'), not str like bar!"]
        err_msg = ("Type of element 2 in tuple (4, 5.0, 'bar') must"
                   " be one of ('int', 'float'), not str like bar!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = AllNum((4, 5.0, 'bar'))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_wrong_unnamed_dict_with_two_types(self):
        AllNum = All(int, float)
        log_msg = ["ERROR:root:Type of key in dict {4: 'four', 'bar': 3}"
                   " must be one of ('int', 'float'), not str like bar!"]
        err_msg = ("Type of key in dict {4: 'four', 'bar': 3} must"
                   " be one of ('int', 'float'), not str like bar!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = AllNum({4: 'four', 'bar': 3})
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_wrong_unnamed_set_with_two_types(self):
        AllNum = All(int, float)
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = AllNum({4, 'bar'})

    def test_error_on_wrong_named_variable_with_two_types(self):
        AllNum = All(int, float)
        log_msg = ["ERROR:root:Type of element 2 in tuple test must"
                   " be one of ('int', 'float'), not str like bar!"]
        err_msg = ("Type of element 2 in tuple test must be one"
                   " of ('int', 'float'), not str like bar!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = AllNum((4, 5.0, 'bar'), 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_wrong_named_dict_with_two_types(self):
        AllNum = All(int, float)
        log_msg = ["ERROR:root:Type of key in dict test must be"
                   " one of ('int', 'float'), not str like bar!"]
        err_msg = ("Type of key in dict test must be one of"
                   " ('int', 'float'), not str like bar!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = AllNum({4: 'four', 5.0: 'five', 'bar': 3}, 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_wrong_named_set_with_two_types(self):
        AllNum = All(int, float)
        log_msg = ["ERROR:root:Type of element in set test must be"
                   " one of ('int', 'float'), not str like bar!"]
        err_msg = ("Type of element in set test must be one of"
                   " ('int', 'float'), not str like bar!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = AllNum({4, 5.0, 'bar'}, 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_has_iterable_type_checker_attributes(self):
        AllNum = All(int, float)
        for iterable in _ITERABLES:
            self.assertTrue(hasattr(AllNum, iterable.__name__))
        self.assertTrue(hasattr(AllNum, 'NonEmpty'))

    def test_iterable_type_checkers_are_type_CompositionOf(self):
        AllNum = All(int, float)
        for iterable in _ITERABLES:
            type_checker = getattr(AllNum, iterable.__name__)
            self.assertIsInstance(type_checker, CompositionOf)
        self.assertIsInstance(AllNum.NonEmpty, CompositionOf)

    def test_has_attribute_NonEmpty(self):
        AllInt = All(int)
        self.assertTrue(hasattr(AllInt, 'NonEmpty'))

    def test_attribute_NonEmpty_is_type_CompositionOf(self):
        AllInt = All(int)
        self.assertIsInstance(AllInt.NonEmpty, CompositionOf)

    def test_works_through_type_and_non_empty_checkers(self):
        AllInt = All(int)
        log_msg = ['ERROR:root:Type of element 1 in tuple '
                   'test must be int, not float like 5.0!']
        err_msg = ('Type of element 1 in tuple test '
                   'must be int, not float like 5.0!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = AllInt.NonEmpty.JustTuple((4, 5.0), 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_through_dict_and_non_empty_checkers(self):
        AllInt = All(int)
        log_msg = ['ERROR:root:Type of key in dict test'
                   ' must be int, not float like 5.0!']
        err_msg = ('Type of key in dict test must'
                   ' be int, not float like 5.0!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = AllInt.NonEmpty.JustDict({4: 'four', 5.0: 'five'}, 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_has_attribute_o(self):
        AllInt = All(int)
        self.assertTrue(hasattr(AllInt, 'o'))

    def test_attribute_o_is_callable(self):
        AllInt = All(int)
        self.assertTrue(callable(AllInt.o))

    def test_o_returns_composition(self):
        AllInt = All(int)
        AllNum = All(int, float)
        composition = AllInt.o(AllNum)
        self.assertIsInstance(composition, CompositionOf)

    def test_o_raises_error_on_argument_not_callable(self):
        AllInt =  All(int)
        err_msg = ('foo must be a callable that accepts (i) a value,'
                   ' (ii) an optional name for that value, and (iii)'
                   ' any number of keyword arguments!')
        with self.assertRaises(CallableError) as err:
            _ = AllInt.o('foo')
        self.assertEqual(str(err.exception), err_msg)


if __name__ == '__main__':
    ut.main()
