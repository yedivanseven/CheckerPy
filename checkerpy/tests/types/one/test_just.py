import logging
import unittest as ut
from collections import defaultdict, deque, OrderedDict
from ....functional import CompositionOf
from ....types.one import Just
from ....exceptions import WrongTypeError, CallableError


class TestJustInstantiation(ut.TestCase):

    def test_error_on_no_types_to_check(self):
        err_msg = 'Found no types to check for!'
        with self.assertRaises(AttributeError) as err:
            _ = Just()
        self.assertEqual(str(err.exception), err_msg)

    def test_error_on_one_type_to_check_wrong_type(self):
        err_msg = 'Type of type specifier foo must be type, not str!'
        with self.assertRaises(TypeError) as err:
            _ = Just('foo')
        self.assertEqual(str(err.exception), err_msg)

    def test_error_on_two_types_to_check_wrong_type(self):
        err_msg = 'Type of type specifier bar must be type, not str!'
        with self.assertRaises(TypeError) as err:
            _ = Just(int, 'bar')
        self.assertEqual(str(err.exception), err_msg)

    def test_error_on_wrong_identifier(self):
        err_msg = 'Type-checker name @baz is not a valid identifier!'
        with self.assertRaises(ValueError) as err:
            _ = Just(int, identifier='@baz')
        self.assertEqual(str(err.exception), err_msg)

    def test_has_default_name(self):
        JustInt = Just(int)
        self.assertEqual(JustInt.__name__, 'Just')

    def test_identifier_sets_name_attribute(self):
        JustInt = Just(int, identifier='JustInt')
        self.assertEqual(JustInt.__name__, 'JustInt')

    def test_has_attribute_types_with_one_valid_type(self):
        JustInt = Just(int)
        self.assertTrue(hasattr(JustInt, 'types'))

    def test_cannot_set_attribute_types(self):
        JustInt = Just(int)
        with self.assertRaises(AttributeError):
            JustInt.types = 'foo'

    def test_attribute_types_has_correct_value_with_one_valid_type(self):
        JustInt = Just(int)
        self.assertTupleEqual(JustInt.types, (int, ))

    def test_works_with_two_valid_types(self):
        _ = Just(int, float)

    def test_has_attribute_types_with_two_valid_types(self):
        JustNum = Just(int, float)
        self.assertTrue(hasattr(JustNum, 'types'))

    def test_attribute_types_has_correct_value_with_two_valid_types(self):
        JustNum = Just(int, float)
        self.assertTupleEqual(JustNum.types, (int, float))

    def test_works_with_types_given_as_tuple(self):
        JustListDict = Just((list, dict))
        self.assertTupleEqual(JustListDict.types, (list, dict))

    def test_works_with_types_given_as_list(self):
        JustBoolStr = Just([bool, str])
        self.assertTupleEqual(JustBoolStr.types, (bool, str))

    def test_works_with_types_given_as_deque(self):
        JustFloatSet = Just(deque([float, set]))
        self.assertTupleEqual(JustFloatSet.types, (float, set))

    def test_works_with_types_given_as_set(self):
        JustIntFloat = Just({int, float})
        self.assertSetEqual(set(JustIntFloat.types), {int, float})

    def test_works_with_types_given_as_frozenset(self):
        JustSliceTuple = Just(frozenset({slice, tuple}))
        self.assertSetEqual(set(JustSliceTuple.types), {slice, tuple})

    def test_works_with_types_given_as_dict(self):
        JustDictInt = Just({dict: 'dict', int: 'int'})
        self.assertSetEqual(set(JustDictInt.types), {dict, int})

    def test_works_with_types_given_as_ordered_dict(self):
        JustDictInt = Just(OrderedDict({dict: 'dict', int: 'int'}))
        self.assertSetEqual(set(JustDictInt.types), {dict, int})

    def test_works_with_types_given_as_defaultdict(self):
        JustDictInt = Just(defaultdict(str, {dict: 'dict', int: 'int'}))
        self.assertSetEqual(set(JustDictInt.types), {dict, int})

    def test_works_with_types_given_as_dict_keys(self):
        JustDictInt = Just({dict: 'dict', int: 'int'}.keys())
        self.assertSetEqual(set(JustDictInt.types), {dict, int})

    def test_works_with_types_given_as_ordered_dict_keys(self):
        JustDictInt = Just(OrderedDict({dict: 'dict', int: 'int'}).keys())
        self.assertSetEqual(set(JustDictInt.types), {dict, int})

    def test_works_with_types_given_as_defaultdict_keys(self):
        JustDictInt = Just(defaultdict(str, {dict: 'dict', int: 'int'}).keys())
        self.assertSetEqual(set(JustDictInt.types), {dict, int})

    def test_works_with_types_given_as_dict_values(self):
        JustDictInt = Just({'dict': dict, 'int': int}.values())
        self.assertSetEqual(set(JustDictInt.types), {dict, int})

    def test_works_with_types_given_as_ordered_dict_values(self):
        JustDictInt = Just(OrderedDict({'dict': dict, 'int': int}).values())
        self.assertSetEqual(set(JustDictInt.types), {dict, int})

    def test_works_with_types_given_as_defaultdict_values(self):
        types = defaultdict(type, {'dict': dict, 'int': int}).values()
        JustDictInt = Just(types)
        self.assertSetEqual(set(JustDictInt.types), {dict, int})


class TestJust(ut.TestCase):

    def test_returns_correct_type_with_one_type(self):
        JustInt = Just(int)
        i = JustInt(1)
        self.assertIsInstance(i, int)

    def test_returns_correct_value_with_one_type(self):
        JustInt = Just(int)
        self.assertEqual(JustInt(2), 2)

    def test_returns_correct_type_with_two_types(self):
        JustNum = Just(int, float)
        i = JustNum(1)
        self.assertIsInstance(i, int)
        f = JustNum(1.0)
        self.assertIsInstance(f, float)

    def test_returns_correct_value_with_two_types(self):
        JustNum = Just(int, float)
        self.assertEqual(JustNum(2), 2)
        self.assertEqual(JustNum(2.0), 2.0)

    def test_error_on_wrong_unnamed_variable_with_one_type(self):
        JustInt = Just(int)
        log_msg = ['ERROR:root:Type must be int, not str like foo!']
        err_msg = 'Type must be int, not str like foo!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = JustInt('foo')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_wrong_named_variable_with_one_type(self):
        JustInt = Just(int)
        log_msg = ['ERROR:root:Type of test must'
                   ' be int, not str like bar!']
        err_msg = 'Type of test must be int, not str like bar!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = JustInt('bar', 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_wrong_unnamed_variable_with_two_types(self):
        JustNum = Just(int, float)
        log_msg = ["ERROR:root:Type must be one of ('int',"
                   " 'float'), not str like foo!"]
        err_msg = "Type must be one of ('int', 'float'), not str like foo!"
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = JustNum('foo')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_wrong_named_variable_with_two_types(self):
        JustNum = Just(int, float)
        log_msg = ["ERROR:root:Type of test must be one of"
                   " ('int', 'float'), not str like bar!"]
        err_msg = ("Type of test must be one of ('int',"
                   " 'float'), not str like bar!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = JustNum('bar', 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)


class TestJustMethods(ut.TestCase):

    def test_has_attribute_o(self):
        JustInt = Just(int)
        self.assertTrue(hasattr(JustInt, 'o'))

    def test_attribute_o_is_callable(self):
        JustInt = Just(int)
        self.assertTrue(callable(JustInt.o))

    def test_o_returns_composition(self):
        JustInt = Just(int)
        JustNum = Just(int, float)
        composition = JustInt.o(JustNum)
        self.assertIsInstance(composition, CompositionOf)

    def test_o_raises_error_on_argument_not_callable(self):
        JustInt = Just(int)
        err_msg = ('foo must be a callable that accepts (i) a value,'
                   ' (ii) an optional name for that value, and (iii)'
                   ' any number of keyword arguments!')
        with self.assertRaises(CallableError) as err:
            _ = JustInt.o('foo')
        self.assertEqual(str(err.exception), err_msg)


if __name__ == '__main__':
    ut.main()

