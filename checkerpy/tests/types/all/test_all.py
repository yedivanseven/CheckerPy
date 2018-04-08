import logging
import unittest as ut
from collections import defaultdict, deque, OrderedDict
from ....functional import CompositionOf
from ....types.all import All
from ....types.one import _REDUCED_ITER
from ....exceptions import WrongTypeError, IterError, CallableError


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


class TestAllWorks(ut.TestCase):

    def test_works_with_str(self):
        AllStr = All(str)
        s = AllStr('foo')
        self.assertIsInstance(s, str)
        self.assertEqual(s, 'foo')

    def test_works_with_tuple(self):
        AllStr = All(str)
        t = AllStr(('f', 'o', 'o'))
        self.assertTupleEqual(t, ('f', 'o', 'o'))

    def test_works_with_list(self):
        AllStr =All(str)
        l = AllStr(['f', 'o', 'o'])
        self.assertListEqual(l, ['f', 'o', 'o'])

    def test_works_with_deque(self):
        AllStr =All(str)
        dq = AllStr(deque(['f', 'o', 'o']))
        self.assertIsInstance(dq, deque)
        self.assertEqual(dq, deque(['f', 'o', 'o']))

    def test_works_with_set(self):
        AllStr = All(str)
        s = AllStr({'f', 'o', 'o'})
        self.assertSetEqual(s, {'f', 'o'})

    def test_works_with_frozenset(self):
        AllStr = All(str)
        s = AllStr(frozenset({'f', 'o', 'o'}))
        self.assertSetEqual(s, {'f', 'o'})

    def test_works_with_dict(self):
        AllStr = All(str)
        d = AllStr({'f': 1, 'o': 2})
        self.assertDictEqual(d, {'f': 1, 'o': 2})

    def test_works_ordered_dict(self):
        AllStr = All(str)
        od = AllStr(OrderedDict({'f': 1, 'o': 2}))
        self.assertIsInstance(od, OrderedDict)
        self.assertDictEqual(od, {'f': 1, 'o': 2})

    def test_works_with_defaultdict(self):
        AllStr = All(str)
        dd = AllStr(defaultdict(int, {'f': 1, 'o': 2}))
        self.assertDictEqual(dd, {'f': 1, 'o': 2})

    def test_works_with_dict_keys(self):
        AllStr = All(str)
        d = AllStr({'f': 1, 'o': 2}.keys())
        self.assertIsInstance(d, type({}.keys()))
        self.assertSetEqual(set(d), set({'f': 1, 'o': 2}.keys()))

    def test_works_with_ordered_dict_keys(self):
        AllStr = All(str)
        od = OrderedDict({'f': 1, 'o': 2})
        output = AllStr(od.keys())
        self.assertIsInstance(output, type(od.keys()))
        self.assertSetEqual(set(od.keys()), set(output))

    def test_works_with_defaultdict_keys(self):
        AllStr = All(str)
        dd = defaultdict(int, {'f': 1, 'o': 2})
        output = AllStr(dd.keys())
        self.assertIsInstance(output, type(dd.keys()))
        self.assertSetEqual(set(dd.keys()), set(output))

    def test_works_with_dict_values(self):
        AllInt = All(int)
        d = AllInt({'f': 1, 'o': 2}.values())
        self.assertIsInstance(d, type({}.values()))
        self.assertSetEqual(set(d), set({'f': 1, 'o': 2}.values()))

    def test_works_with_ordered_dict_values(self):
        AllInt = All(int)
        od = OrderedDict({'f': 1, 'o': 2})
        output = AllInt(od.values())
        self.assertIsInstance(output, type(od.values()))
        self.assertSetEqual(set(od.values()), set(output))

    def test_works_with_defaultdict_values(self):
        AllInt = All(int)
        dd = defaultdict(int, {'f': 1, 'o': 2})
        output = AllInt(dd.values())
        self.assertIsInstance(output, type(dd.values()))
        self.assertSetEqual(set(dd.values()), set(output))

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


class TestAllErrorUnnamedOneType(ut.TestCase):

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

    def test_error_on_wrong_unnamed_tuple_with_one_type(self):
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

    def test_error_on_wrong_unnamed_list_with_one_type(self):
        AllInt = All(int)
        log_msg = ['ERROR:root:Type of element 1 in list [4,'
                   ' 5.0] must be int, not float like 5.0!']
        err_msg = ('Type of element 1 in list [4, 5.0]'
                   ' must be int, not float like 5.0!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = AllInt([4, 5.0])
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_wrong_unnamed_deque_with_one_type(self):
        AllInt = All(int)
        log_msg = ['ERROR:root:Type of element 1 in deque([4,'
                   ' 5.0]) must be int, not float like 5.0!']
        err_msg = ('Type of element 1 in deque([4, 5.0])'
                   ' must be int, not float like 5.0!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = AllInt(deque([4, 5.0]))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_wrong_unnamed_dict_with_one_type(self):
        AllInt = All(int)
        inputs = {4: 'four', 5.0: 'five'}
        log_msg = ["ERROR:root:Type of key in dict {4: 'four', "
                   "5.0: 'five'} must be int, not float like 5.0!"]
        err_msg = ("Type of key in dict {4: 'four', 5.0: "
                   "'five'} must be int, not float like 5.0!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = AllInt(inputs)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_wrong_unnamed_ordered_dict_with_one_type(self):
        AllInt = All(int)
        inputs = OrderedDict({4: 'four', 5.0: 'five'})
        log_msg = ["ERROR:root:Type of key in OrderedDict([(4, 'four'),"
                   " (5.0, 'five')]) must be int, not float like 5.0!"]
        err_msg = ("Type of key in OrderedDict([(4, 'four'), (5.0,"
                   " 'five')]) must be int, not float like 5.0!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = AllInt(inputs)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_wrong_unnamed_defaultdict_with_one_type(self):
        AllInt = All(int)
        inputs = defaultdict(str, {4: 'four', 5.0: 'five'})
        log_msg = ["ERROR:root:Type of key in defaultdict(<class 'str'>, {4:"
                   " 'four', 5.0: 'five'}) must be int, not float like 5.0!"]
        err_msg = ("Type of key in defaultdict(<class 'str'>, {4: 'four',"
                   " 5.0: 'five'}) must be int, not float like 5.0!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = AllInt(inputs)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_wrong_unnamed_dict_key_with_one_type(self):
        AllInt = All(int)
        log_msg = ['ERROR:root:Type of key in dict_keys([4,'
                   ' 5.0]) must be int, not float like 5.0!']
        err_msg = ('Type of key in dict_keys([4, 5.0])'
                   ' must be int, not float like 5.0!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = AllInt({4: 'four', 5.0: 'five'}.keys())
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_wrong_unnamed_ordered_dict_key_with_one_type(self):
        AllInt = All(int)
        inputs = OrderedDict({4: 'four', 5.0: 'five'})
        log_msg = ['ERROR:root:Type of key in odict_keys([4,'
                   ' 5.0]) must be int, not float like 5.0!']
        err_msg = ('Type of key in odict_keys([4, 5.0])'
                   ' must be int, not float like 5.0!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = AllInt(inputs.keys())
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_wrong_unnamed_defaultdict_key_with_one_type(self):
        AllInt = All(int)
        inputs = defaultdict(str, {4: 'four', 5.0: 'five'})
        log_msg = ['ERROR:root:Type of key in dict_keys([4,'
                   ' 5.0]) must be int, not float like 5.0!']
        err_msg = ('Type of key in dict_keys([4, 5.0])'
                   ' must be int, not float like 5.0!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = AllInt(inputs.keys())
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_wrong_unnamed_dict_values_with_one_type(self):
        AllStr = All(str)
        log_msg = ["ERROR:root:Type of value in dict_values(['four', 5])"
                   " must be str, not int like 5!"]
        err_msg = ("Type of value in dict_values(['four', 5])"
                   " must be str, not int like 5!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = AllStr({4: 'four', 5.0: 5}.values())
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_wrong_unnamed_ordered_dict_values_with_one_type(self):
        AllStr = All(str)
        inputs = OrderedDict({4: 'four', 5.0: 5})
        log_msg = ["ERROR:root:Type of value in odict_values(['four', 5])"
                   " must be str, not int like 5!"]
        err_msg = ("Type of value in odict_values(['four', 5])"
                   " must be str, not int like 5!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = AllStr(inputs.values())
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_wrong_unnamed_defaultdict_values_with_one_type(self):
        AllStr = All(str)
        inputs = defaultdict(str, {4: 'four', 5.0: 5})
        log_msg = ["ERROR:root:Type of value in dict_values(['four', 5])"
                   " must be str, not int like 5!"]
        err_msg = ("Type of value in dict_values(['four', 5])"
                   " must be str, not int like 5!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = AllStr(inputs.values())
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

    def test_error_on_wrong_unnamed_frozenset_with_one_type(self):
        AllInt = All(int)
        log_msg = ["ERROR:root:Type of element in frozenset({4, "
                   "5.0}) must be int, not float like 5.0!"]
        err_msg = ("Type of element in frozenset({4, 5.0}) must"
                   " be int, not float like 5.0!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = AllInt(frozenset({4, 5.0}))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)


class TestAllErrorNamedOneType(ut.TestCase):

    def test_error_on_wrong_named_tuple_with_one_type(self):
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

    def test_error_on_wrong_named_list_with_one_type(self):
        AllInt = All(int)
        log_msg = ['ERROR:root:Type of element 1 in list '
                   'test must be int, not float like 5.0!']
        err_msg = ('Type of element 1 in list test '
                   'must be int, not float like 5.0!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = AllInt([4, 5.0], 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_wrong_named_deque_with_one_type(self):
        AllInt = All(int)
        log_msg = ['ERROR:root:Type of element 1 in deque '
                   'test must be int, not float like 5.0!']
        err_msg = ('Type of element 1 in deque test '
                   'must be int, not float like 5.0!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = AllInt(deque([4, 5.0]), 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_wrong_named_dict_with_one_type(self):
        AllInt = All(int)
        inputs = {4: 'four', 5.0: 'five'}
        log_msg = ['ERROR:root:Type of key in dict test'
                   ' must be int, not float like 5.0!']
        err_msg = ('Type of key in dict test must'
                   ' be int, not float like 5.0!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = AllInt(inputs, 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_wrong_named_ordered_dict_with_one_type(self):
        AllInt = All(int)
        inputs = OrderedDict({4: 'four', 5.0: 'five'})
        log_msg = ['ERROR:root:Type of key in OrderedDict test'
                   ' must be int, not float like 5.0!']
        err_msg = ('Type of key in OrderedDict test must'
                   ' be int, not float like 5.0!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = AllInt(inputs, 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_wrong_named_defaultdict_with_one_type(self):
        AllInt = All(int)
        inputs = defaultdict(str, {4: 'four', 5.0: 'five'})
        log_msg = ['ERROR:root:Type of key in defaultdict test'
                   ' must be int, not float like 5.0!']
        err_msg = ('Type of key in defaultdict test must'
                   ' be int, not float like 5.0!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = AllInt(inputs, 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_wrong_named_dict_keys_with_one_type(self):
        AllInt = All(int)
        inputs = {4: 'four', 5.0: 'five'}
        log_msg = ['ERROR:root:Type of key in dict test'
                   ' must be int, not float like 5.0!']
        err_msg = ('Type of key in dict test must'
                   ' be int, not float like 5.0!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = AllInt(inputs.keys(), 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_wrong_named_ordered_dict_keys_with_one_type(self):
        AllInt = All(int)
        inputs = OrderedDict({4: 'four', 5.0: 'five'})
        log_msg = ['ERROR:root:Type of key in dict test'
                   ' must be int, not float like 5.0!']
        err_msg = ('Type of key in dict test must'
                   ' be int, not float like 5.0!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = AllInt(inputs.keys(), 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_wrong_named_defaultdict_keys_with_one_type(self):
        AllInt = All(int)
        inputs = defaultdict(str, {4: 'four', 5.0: 'five'})
        log_msg = ['ERROR:root:Type of key in dict test'
                   ' must be int, not float like 5.0!']
        err_msg = ('Type of key in dict test must'
                   ' be int, not float like 5.0!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = AllInt(inputs.keys(), 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_wrong_named_dict_values_with_one_type(self):
        AllStr = All(str)
        inputs = {4: 'four', 5.0: 5}
        log_msg = ['ERROR:root:Type of value in dict '
                   'test must be str, not int like 5!']
        err_msg = ('Type of value in dict test '
                   'must be str, not int like 5!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = AllStr(inputs.values(), 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_wrong_named_ordered_dict_values_with_one_type(self):
        AllStr = All(str)
        inputs = OrderedDict({4: 'four', 5.0: 5})
        log_msg = ['ERROR:root:Type of value in dict '
                   'test must be str, not int like 5!']
        err_msg = ('Type of value in dict test '
                   'must be str, not int like 5!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = AllStr(inputs.values(), 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_wrong_named_defaultdict_values_with_one_type(self):
        AllStr = All(str)
        inputs = defaultdict(str, {4: 'four', 5.0: 5})
        log_msg = ['ERROR:root:Type of value in dict '
                   'test must be str, not int like 5!']
        err_msg = ('Type of value in dict test '
                   'must be str, not int like 5!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = AllStr(inputs.values(), 'test')
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

    def test_error_on_wrong_named_frozenset_with_one_type(self):
        AllInt = All(int)
        log_msg = ['ERROR:root:Type of element in frozenset test'
                   ' must be int, not float like 5.0!']
        err_msg = ('Type of element in frozenset test must'
                   ' be int, not float like 5.0!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = AllInt(frozenset({4, 5.0}), 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)


class TestAllErrorTowTypes(ut.TestCase):

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

    def test_error_on_wrong_unnamed_dict_key_with_two_types(self):
        AllNum = All(int, float)
        log_msg = ["ERROR:root:Type of key in dict_keys([4, 'bar'])"
                   " must be one of ('int', 'float'), not str like bar!"]
        err_msg = ("Type of key in dict_keys([4, 'bar']) must"
                   " be one of ('int', 'float'), not str like bar!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = AllNum({4: 'four', 'bar': 3}.keys())
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_wrong_unnamed_dict_value_with_two_types(self):
        AllNum = All(int, float)
        log_msg = ["ERROR:root:Type of value in dict_values(['four', 3])"
                   " must be one of ('int', 'float'), not str like four!"]
        err_msg = ("Type of value in dict_values(['four', 3]) must"
                   " be one of ('int', 'float'), not str like four!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = AllNum({4: 'four', 'bar': 3}.values())
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_wrong_unnamed_set_with_two_types(self):
        AllNum = All(int, float)
        with self.assertLogs(level=logging.ERROR):
            with self.assertRaises(WrongTypeError):
                _ = AllNum({4, 'bar'})

    def test_error_on_wrong_unnamed_frozenset_with_two_types(self):
        AllNum = All(int, float)
        with self.assertLogs(level=logging.ERROR):
            with self.assertRaises(WrongTypeError):
                _ = AllNum(frozenset({4, 'bar'}))

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

    def test_error_on_wrong_named_dict_key_with_two_types(self):
        AllNum = All(int, float)
        log_msg = ["ERROR:root:Type of key in dict test must be"
                   " one of ('int', 'float'), not str like bar!"]
        err_msg = ("Type of key in dict test must be one of"
                   " ('int', 'float'), not str like bar!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = AllNum({4: 'four', 5.0: 'five', 'bar': 3}.keys(), 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_wrong_named_dict_value_with_two_types(self):
        AllNum = All(int, float)
        log_msg = ["ERROR:root:Type of value in dict test must be"
                   " one of ('int', 'float'), not str like four!"]
        err_msg = ("Type of value in dict test must be one of"
                   " ('int', 'float'), not str like four!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = AllNum({4: 'four', 5.0: 'five', 'bar': 3}.values(), 'test')
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

    def test_error_on_wrong_named_frozenset_with_two_types(self):
        AllNum = All(int, float)
        log_msg = ["ERROR:root:Type of element in frozenset test must be"
                   " one of ('int', 'float'), not str like bar!"]
        err_msg = ("Type of element in frozenset test must be one of"
                   " ('int', 'float'), not str like bar!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = AllNum(frozenset({4, 5.0, 'bar'}), 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)


class TestAllMethods(ut.TestCase):

    def test_has_iterable_type_checker_attributes(self):
        AllNum = All(int, float)
        for iterable in _REDUCED_ITER:
            self.assertTrue(hasattr(AllNum, iterable.__name__))
        self.assertTrue(hasattr(AllNum, 'NonEmpty'))

    def test_iterable_type_checkers_are_type_CompositionOf(self):
        AllNum = All(int, float)
        for iterable in _REDUCED_ITER:
            type_checker = getattr(AllNum, iterable.__name__)
            self.assertIsInstance(type_checker, CompositionOf)
        self.assertIsInstance(AllNum.NonEmpty, CompositionOf)

    def test_has_attribute_NonEmpty(self):
        AllInt = All(int)
        self.assertTrue(hasattr(AllInt, 'NonEmpty'))

    def test_attribute_NonEmpty_is_type_CompositionOf(self):
        AllInt = All(int)
        self.assertIsInstance(AllInt.NonEmpty, CompositionOf)

    def test_has_attribute_JustLen(self):
        AllInt = All(int)
        self.assertTrue(hasattr(AllInt, 'JustLen'))

    def test_attribute_JustLen_is_type_CompositionOf(self):
        AllInt = All(int)
        self.assertIsInstance(AllInt.JustLen, CompositionOf)

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

    def test_works_through_dict_and_just_length_checkers(self):
        AllInt = All(int)
        inputs = {4: 'four', 5.0: 'five'}
        log_msg = ['ERROR:root:Type of key in dict test'
                   ' must be int, not float like 5.0!']
        err_msg = ('Type of key in dict test must'
                   ' be int, not float like 5.0!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = AllInt.JustLen.JustDict(inputs, 'test', length=2)
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
        AllInt = All(int)
        err_msg = ('foo must be a callable that accepts (i) a value,'
                   ' (ii) an optional name for that value, and (iii)'
                   ' any number of keyword arguments!')
        with self.assertRaises(CallableError) as err:
            _ = AllInt.o('foo')
        self.assertEqual(str(err.exception), err_msg)


if __name__ == '__main__':
    ut.main()
