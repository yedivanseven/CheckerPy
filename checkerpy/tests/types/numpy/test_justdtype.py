import logging
import unittest as ut
from collections import defaultdict, deque, OrderedDict
from ....functional import CompositionOf
from ....exceptions import WrongTypeError, DtypeError, CallableError
try:
    from ....types.numpy import JustDtype, JustNdarray
    from numpy import int16, int32, float32, dtype
except ImportError:
    no_numpy = True
else:
    no_numpy = False


@ut.skipIf(no_numpy, 'Could not import numpy!')
class TestJustDtypeInstatiation(ut.TestCase):

    def test_error_on_no_types_to_check(self):
        err_msg = 'Found no types to check for!'
        with self.assertRaises(AttributeError) as err:
            _ = JustDtype()
        self.assertEqual(str(err.exception), err_msg)

    def test_error_on_one_type_to_check_wrong_type_as_attribute(self):
        err_msg = 'Type of type specifier foo must be type, not str!'
        with self.assertRaises(TypeError) as err:
            _ = JustDtype('foo')
        self.assertEqual(str(err.exception), err_msg)

    def test_error_on_two_types_to_check_wrong_type(self):
        err_msg = 'Type of type specifier bar must be type, not str!'
        with self.assertRaises(TypeError) as err:
            _ = JustDtype(int16, 'bar')
        self.assertEqual(str(err.exception), err_msg)

    def test_error_on_wrong_identifier(self):
        err_msg = 'Dtype-checker name @baz is not a valid identifier!'
        with self.assertRaises(ValueError) as err:
            _ = JustDtype(int16, identifier='@baz')
        self.assertEqual(str(err.exception), err_msg)

    def test_has_default_name(self):
        JustInt16 = JustDtype(int16)
        self.assertEqual(JustInt16.__name__, 'JustD')

    def test_identifier_sets_name_attribute(self):
        JustInt16 = JustDtype(int16, identifier='JustInt16')
        self.assertEqual(JustInt16.__name__, 'JustInt16')

    def test_has_attribute_dtypes_with_one_valid_type(self):
        JustInt16 = JustDtype(int16)
        self.assertTrue(hasattr(JustInt16, 'dtypes'))

    def test_cannot_set_attribute_dtypes(self):
        JustInt16 = JustDtype(int16)
        with self.assertRaises(AttributeError):
            JustInt16.dtypes = 'foo'

    def test_attribute_dtypes_has_correct_value_with_one_valid_type(self):
        JustInt16 = JustDtype(int16)
        self.assertTupleEqual(JustInt16.dtypes, (int16, ))

    def test_works_with_two_valid_types(self):
        _ = JustDtype(int16, float32)

    def test_has_attribute_dtypes_with_two_valid_types(self):
        JustNpNum = JustDtype(int16, float32)
        self.assertTrue(hasattr(JustNpNum, 'dtypes'))

    def test_attribute_dtypes_has_correct_value_with_two_valid_types(self):
        JustNpNum = JustDtype(int16, float32)
        self.assertTupleEqual(JustNpNum.dtypes, (int16, float32))

    def test_works_with_types_given_as_tuple(self):
        JustInt16Float32 = JustDtype((int16, float32))
        self.assertTupleEqual(JustInt16Float32.dtypes, (int16, float32))

    def test_works_with_types_given_as_list(self):
        JustInt16Float32 = JustDtype([int16, float32])
        self.assertTupleEqual(JustInt16Float32.dtypes, (int16, float32))

    def test_works_with_types_given_as_deque(self):
        JustInt16Float32 = JustDtype(deque([int16, float32]))
        self.assertTupleEqual(JustInt16Float32.dtypes, (int16, float32))

    def test_works_with_types_given_as_set(self):
        JustInt16Float32 = JustDtype({int16, float32})
        self.assertSetEqual(set(JustInt16Float32.dtypes),
                            {dtype('int16'), dtype('float32')})

    def test_works_with_types_given_as_frozenset(self):
        JustInt16Float32 = JustDtype(frozenset({int16, float32}))
        self.assertSetEqual(set(JustInt16Float32.dtypes),
                            {dtype('int16'), dtype('float32')})

    def test_works_with_types_given_as_dict(self):
        types = {int16: 'int16', float32: 'float32'}
        JustInt16Float32 = JustDtype(types)
        self.assertSetEqual(set(JustInt16Float32.dtypes),
                            {dtype('int16'), dtype('float32')})

    def test_works_with_types_given_as_ordered_dict(self):
        types = OrderedDict({int16: 'int16', float32: 'float32'})
        JustInt16Float32 = JustDtype(types)
        self.assertSetEqual(set(JustInt16Float32.dtypes),
                            {dtype('int16'), dtype('float32')})

    def test_works_with_types_given_as_defaultdict(self):
        types = defaultdict(str, {int16: 'int16', float32: 'float32'})
        JustInt16Float32 = JustDtype(types)
        self.assertSetEqual(set(JustInt16Float32.dtypes),
                            {dtype('int16'), dtype('float32')})

    def test_works_with_types_given_as_dict_keys(self):
        types = {int16: 'int16', float32: 'float32'}.keys()
        JustInt16Float32 = JustDtype(types)
        self.assertSetEqual(set(JustInt16Float32.dtypes),
                            {dtype('int16'), dtype('float32')})

    def test_works_with_types_given_as_ordered_dict_keys(self):
        types = OrderedDict({int16: 'int16', float32: 'float32'}).keys()
        JustInt16Float32 = JustDtype(types)
        self.assertSetEqual(set(JustInt16Float32.dtypes),
                            {dtype('int16'), dtype('float32')})

    def test_works_with_types_given_as_defaultdict_keys(self):
        types = defaultdict(str, {int16: 'int16', float32: 'float32'}).keys()
        JustInt16Float32 = JustDtype(types)
        self.assertSetEqual(set(JustInt16Float32.dtypes),
                            {dtype('int16'), dtype('float32')})

    def test_works_with_types_given_as_dict_values(self):
        types = {'int16': int16, 'float32': float32}.values()
        JustInt16Float32 = JustDtype(types)
        self.assertSetEqual(set(JustInt16Float32.dtypes),
                            {dtype('int16'), dtype('float32')})

    def test_works_with_types_given_as_ordered_dict_values(self):
        types = OrderedDict({'int16': int16, 'float32': float32}).values()
        JustInt16Float32 = JustDtype(types)
        self.assertSetEqual(set(JustInt16Float32.dtypes),
                            {dtype('int16'), dtype('float32')})

    def test_works_with_types_given_as_defaultdict_values(self):
        types = defaultdict(type, {'int16': int16, 'float32': float32})
        JustInt16Float32 = JustDtype(types.values())
        self.assertSetEqual(set(JustInt16Float32.dtypes),
                            {dtype('int16'), dtype('float32')})


@ut.skipIf(no_numpy, 'Could not import numpy!')
class TestJustDtype(ut.TestCase):

    def test_returns_correct_type_with_one_type(self):
        JustInt16 = JustDtype(int16)
        i = JustInt16(int16(1))
        self.assertIsInstance(i, int16)

    def test_returns_correct_value_with_one_type(self):
        JustInt16 = JustDtype(int16)
        self.assertEqual(JustInt16(int16(2)), int16(2))

    def test_returns_correct_type_with_two_types(self):
        JustNpNum = JustDtype(int16, float32)
        i = JustNpNum(int16(1))
        self.assertIsInstance(i, int16)
        f = JustNpNum(float32(1.0))
        self.assertIsInstance(f, float32)

    def test_returns_correct_value_with_two_types(self):
        JustNpNum = JustDtype(int16, float32)
        self.assertEqual(JustNpNum(int16(2)), int16(2))
        self.assertEqual(JustNpNum(float32(2.0)), float32(2.0))

    def test_error_on_unnamed_variable_no_dtype(self):
        JustInt16 = JustDtype(int16)
        log_msg = ['ERROR:root:Variable foo of type'
                   ' str has no attribute dtype!']
        err_msg = 'Variable foo of type str has no attribute dtype!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(DtypeError) as err:
                _ = JustInt16('foo')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_variable_no_dtype(self):
        JustInt16 = JustDtype(int16)
        log_msg = ['ERROR:root:Variable test of type'
                   ' str has no attribute dtype!']
        err_msg = 'Variable test of type str has no attribute dtype!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(DtypeError) as err:
                _ = JustInt16('bar', 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_wrong_unnamed_variable_with_one_type(self):
        JustInt16 = JustDtype(int16)
        log_msg = ['ERROR:root:Dtype must be int16, not float32 like 1.0!']
        err_msg = 'Dtype must be int16, not float32 like 1.0!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = JustInt16(float32(1.0))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_wrong_named_variable_with_one_type(self):
        JustInt16 = JustDtype(int16)
        log_msg = ['ERROR:root:Dtype of test must be'
                   ' int16, not float32 like 2.0!']
        err_msg = 'Dtype of test must be int16, not float32 like 2.0!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = JustInt16(float32(2.0), 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_wrong_unnamed_variable_with_two_types(self):
        JustNpNum = JustDtype(int16, float32)
        log_msg = ["ERROR:root:Dtype must be one of ('int16',"
                   " 'float32'), not int32 like 1!"]
        err_msg = ("Dtype must be one of ('int16', "
                   "'float32'), not int32 like 1!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = JustNpNum(int32(1))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_wrong_named_variable_with_two_types(self):
        JustNpNum = JustDtype(int16, float32)
        log_msg = ["ERROR:root:Dtype of test must be one of "
                   "('int16', 'float32'), not int32 like 2!"]
        err_msg = ("Dtype of test must be one of ('int16', "
                   "'float32'), not int32 like 2!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = JustNpNum(int32(2), 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)


@ut.skipIf(no_numpy, 'Could not import numpy!')
class TestJustDtypeMethods(ut.TestCase):

    def test_has_attribute_JustNdarray(self):
        JustInt16 = JustDtype(int16)
        self.assertTrue(hasattr(JustInt16, 'JustNdarray'))

    def test_attribute_JustNdarray_is_type_CompositionOf(self):
        JustInt16 = JustDtype(int16)
        self.assertIsInstance(JustInt16.JustNdarray, CompositionOf)

    def test_has_attribute_o(self):
        JustInt16 = JustDtype(int16)
        self.assertTrue(hasattr(JustInt16, 'o'))

    def test_attribute_o_is_callable(self):
        JustInt16 = JustDtype(int16)
        self.assertTrue(callable(JustInt16.o))

    def test_o_returns_composition(self):
        JustInt16 = JustDtype(int16)
        JustNpNum = JustDtype(int16, float32)
        composition = JustInt16.o(JustNpNum)
        self.assertIsInstance(composition, CompositionOf)

    def test_o_raises_error_on_argument_not_callable(self):
        JustInt16 = JustDtype(int16)
        err_msg = ('foo must be a callable that accepts (i) a value,'
                   ' (ii) an optional name for that value, and (iii)'
                   ' any number of keyword arguments!')
        with self.assertRaises(CallableError) as err:
            _ = JustInt16.o('foo')
        self.assertEqual(str(err.exception), err_msg)


if __name__ == '__main__':
    ut.main()
