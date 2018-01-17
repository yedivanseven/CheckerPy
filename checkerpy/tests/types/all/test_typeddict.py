import logging
import unittest as ut
from ....functional import CompositionOf
from ....types.all import TypedDict
from ....exceptions import WrongTypeError


class TestTypedDict(ut.TestCase):

    def test_works_with_no_key_or_value_types(self):
        inp = {1: 'one', 2: 'two', 3: 'three'}
        out = TypedDict(inp)
        self.assertDictEqual(out, inp)

    def test_works_with_keys_ellipsis(self):
        inp = {1: 'one', 2: 'two', 3: 'three'}
        out = TypedDict(inp, keys=...)
        self.assertDictEqual(out, inp)

    def test_works_with_values_ellipsis(self):
        inp = {1: 'one', 2: 'two', 3: 'three'}
        out = TypedDict(inp, values=...)
        self.assertDictEqual(out, inp)

    def test_works_with_keys_and_values_ellipsis(self):
        inp = {1: 'one', 2: 'two', 3: 'three'}
        out = TypedDict(inp, keys=..., values=...)
        self.assertDictEqual(out, inp)

    def test_works_with_keys_false(self):
        inp = {1: 'one', 2: 'two', 3: 'three'}
        out = TypedDict(inp, keys=False)
        self.assertDictEqual(out, inp)

    def test_works_with_values_false(self):
        inp = {1: 'one', 2: 'two', 3: 'three'}
        out = TypedDict(inp, values=0)
        self.assertDictEqual(out, inp)

    def test_works_with_keys_and_values_false(self):
        inp = {1: 'one', 2: 'two', 3: 'three'}
        out = TypedDict(inp, keys=(), values=False)
        self.assertDictEqual(out, inp)

    def test_error_on_keys_type_wrong(self):
        inp = {1: 'one', 2: 'two', 3: 'three'}
        err_msg = 'Type of type specifier 4 must be type, not int!'
        with self.assertRaises(TypeError) as err:
            _ = TypedDict(inp, keys=4)
        self.assertEqual(str(err.exception), err_msg)

    def test_error_on_values_type_wrong(self):
        inp = {1: 'one', 2: 'two', 3: 'three'}
        err_msg = 'Type of type specifier foo must be type, not str!'
        with self.assertRaises(TypeError) as err:
            _ = TypedDict(inp, values='foo')
        self.assertEqual(str(err.exception), err_msg)

    def test_error_on_keys_and_values_type_wrong(self):
        inp = {1: 'one', 2: 'two', 3: 'three'}
        err_msg = 'Type of type specifier 4 must be type, not int!'
        with self.assertRaises(TypeError) as err:
            _ = TypedDict(inp, keys=4, values='foo')
        self.assertEqual(str(err.exception), err_msg)

    def test_error_on_unnamed_argument_not_dict(self):
        inp = {1, 2, 3}
        log_msg = ['ERROR:root:Type must be dict, not set like {1, 2, 3}!']
        err_msg = 'Type must be dict, not set like {1, 2, 3}!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = TypedDict(inp, keys=int, values=float)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_argument_not_dict(self):
        inp = {1, 2, 3}
        log_msg = ['ERROR:root:Type of test must be'
                   ' dict, not set like {1, 2, 3}!']
        err_msg = 'Type of test must be dict, not set like {1, 2, 3}!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = TypedDict(inp, 'test', keys=int, values=float)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_single_type_for_keys(self):
        inp = {1: 'one', 2: 'two', 3: 'three'}
        out = TypedDict(inp, keys=int)
        self.assertDictEqual(out, inp)

    def test_works_with_single_type_for_values(self):
        inp = {1: 'one', 2: 'two', 3: 'three'}
        out = TypedDict(inp, values=str)
        self.assertDictEqual(out, inp)

    def test_works_with_single_type_for_keys_and_values(self):
        inp = {1: 'one', 2: 'two', 3: 'three'}
        out = TypedDict(inp, keys=int, values=str)
        self.assertDictEqual(out, inp)

    def test_error_on_unnamed_wrong_key_single_type(self):
        inp = {1: 'one', 2.0: 'two', 3: 'three'}
        log_msg = ["ERROR:root:Type of key in dict {1: 'one', 2.0:"
                   " 'two', 3: 'three'} must be int, not float like 2.0!"]
        err_msg = ("Type of key in dict {1: 'one', 2.0: 'two',"
                   " 3: 'three'} must be int, not float like 2.0!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = TypedDict(inp, keys=int, values=str)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_wrong_key_single_type(self):
        inp = {1: 'one', 2.0: 'two', 3: 'three'}
        log_msg = ['ERROR:root:Type of key in dict '
                   'test must be int, not float like 2.0!']
        err_msg = ('Type of key in dict test must'
                   ' be int, not float like 2.0!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = TypedDict(inp, 'test', keys=int, values=str)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_unnamed_wrong_value_single_type(self):
        inp = {1: 'one', 2: False, 3: 'three'}
        log_msg = ["ERROR:root:Type of entry 2 in dict {1: 'one', 2:"
                   " False, 3: 'three'} must be str, not bool like False!"]
        err_msg = ("Type of entry 2 in dict {1: 'one', 2: False,"
                   " 3: 'three'} must be str, not bool like False!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = TypedDict(inp, keys=int, values=str)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_wrong_value_single_type(self):
        inp = {1: 'one', 2: False, 3: 'three'}
        log_msg = ['ERROR:root:Type of entry 2 in dict '
                   'test must be str, not bool like False!']
        err_msg = ('Type of entry 2 in dict test '
                   'must be str, not bool like False!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = TypedDict(inp, 'test', keys=int, values=str)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_unnamed_wrong_key_multiple_types(self):
        inp = {1: 'one', 2.0: 'two', 3: 'three'}
        log_msg = ["ERROR:root:Type of key in dict {1:"
                   " 'one', 2.0: 'two', 3: 'three'} must be "
                   "one of ('int', 'bool'), not float like 2.0!"]
        err_msg = ("Type of key in dict {1: 'one',"
                   " 2.0: 'two', 3: 'three'} must be one "
                   "of ('int', 'bool'), not float like 2.0!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = TypedDict(inp, keys=(int, bool), values=...)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_wrong_key_multiple_types(self):
        inp = {1: 'one', 2.0: 'two', 3: 'three'}
        log_msg = ["ERROR:root:Type of key in dict test must "
                   "be one of ('int', 'bool'), not float like 2.0!"]
        err_msg = ("Type of key in dict test must be one"
                   " of ('int', 'bool'), not float like 2.0!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = TypedDict(inp, 'test', keys=(int, bool), values=0)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_unnamed_wrong_value_multiple_types(self):
        inp = {1: 'one', 2: False, 3: 'three'}
        log_msg = ["ERROR:root:Type of entry 2 in dict {1:"
                   " 'one', 2: False, 3: 'three'} must be one of"
                   " ('str', 'int'), not bool like False!"]
        err_msg = ("Type of entry 2 in dict {1: 'one',"
                   " 2: False, 3: 'three'} must be one of "
                   "('str', 'int'), not bool like False!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = TypedDict(inp, keys=[], values=(str, int))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_wrong_value_multiple_types(self):
        inp = {1: 'one', 2: False, 3: 'three'}
        log_msg = ["ERROR:root:Type of entry 2 in dict test must"
                   " be one of ('str', 'int'), not bool like False!"]
        err_msg = ("Type of entry 2 in dict test must be "
                   "one of ('str', 'int'), not bool like False!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = TypedDict(inp, 'test', keys=False, values=(str, int))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_wrong_key_and_values_multiple_types(self):
        inp = {1: 'one', 2.0: 'two', 3: True}
        log_msg = ["ERROR:root:Type of key in dict test must "
                   "be one of ('int', 'bool'), not float like 2.0!"]
        err_msg = ("Type of key in dict test must be one"
                   " of ('int', 'bool'), not float like 2.0!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = TypedDict(inp, 'test', keys=(int, bool), values=(str, int))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_has_attribute_o(self):
        self.assertTrue(hasattr(TypedDict, 'o'))

    def test_attribute_o_is_callable(self):
        self.assertTrue(callable(TypedDict.o))

    def test_o_returns_composition(self):
        def f(x):
            return x
        composition = TypedDict.o(f)
        self.assertIsInstance(composition, CompositionOf)

    def test_has_attribute_JustLen(self):
        self.assertTrue(hasattr(TypedDict, 'JustLen'))

    def test_attribute_JustLen_is_CompositionOf(self):
        self.assertIsInstance(TypedDict.JustLen, CompositionOf)

    def test_keys_and_values_piped_through_JustLen(self):
        inp = {1: 'one', 2: False, 3: 'three'}
        log_msg = ["ERROR:root:Type of entry 2 in dict {1: 'one', 2:"
                   " False, 3: 'three'} must be str, not bool like False!"]
        err_msg = ("Type of entry 2 in dict {1: 'one', 2: False,"
                   " 3: 'three'} must be str, not bool like False!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = TypedDict.JustLen(inp, length=3, keys=int, values=str)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_has_attribute_NonEmpty(self):
        self.assertTrue(hasattr(TypedDict, 'NonEmpty'))

    def test_attribute_NonEmpty_is_CompositionOf(self):
        self.assertIsInstance(TypedDict.NonEmpty, CompositionOf)

    def test_keys_and_values_piped_through_NonEmpty(self):
        inp = {1: 'one', 2: False, 3: 'three'}
        log_msg = ["ERROR:root:Type of entry 2 in dict {1: 'one', 2:"
                   " False, 3: 'three'} must be str, not bool like False!"]
        err_msg = ("Type of entry 2 in dict {1: 'one', 2: False,"
                   " 3: 'three'} must be str, not bool like False!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = TypedDict.NonEmpty(inp, keys=int, values=str)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)


if __name__ == '__main__':
    ut.main()
