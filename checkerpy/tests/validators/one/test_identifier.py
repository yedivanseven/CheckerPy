import logging
import unittest as ut
from collections import defaultdict, deque, OrderedDict
from ....validators.one import Identifier
from ....exceptions import IdentifierError, CallableError
from ....functional import CompositionOf


class TestIdentifier(ut.TestCase):

    def test_works_with_sane_identifier(self):
        inp = 'test'
        out = Identifier(inp)
        self.assertEqual(out, inp)

    def test_error_on_unnamed_str_not_identifier(self):
        log_msg = ['ERROR:root:1 is not a valid identifier!']
        err_msg = '1 is not a valid identifier!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(IdentifierError) as err:
                _ = Identifier('1')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_str_not_identifier(self):
        log_msg = ['ERROR:root:Value 1 of str test is not a valid identifier!']
        err_msg = 'Value 1 of str test is not a valid identifier!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(IdentifierError) as err:
                _ = Identifier('1', 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_unnamed_arg_not_str(self):
        log_msg = ['ERROR:root:int 1 is not a valid identifier!']
        err_msg = 'int 1 is not a valid identifier!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(IdentifierError) as err:
                _ = Identifier(1)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_arg_not_str(self):
        log_msg = ['ERROR:root:int test is not a valid identifier!']
        err_msg = 'int test is not a valid identifier!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(IdentifierError) as err:
                _ = Identifier(1, 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_unnamed_frozenset(self):
        inp = frozenset({1, 2})
        log_msg = ['ERROR:root:frozenset({1, 2}) is not a valid identifier!']
        err_msg = 'frozenset({1, 2}) is not a valid identifier!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(IdentifierError) as err:
                _ = Identifier(inp)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_frozenset(self):
        inp = frozenset({1, 2})
        log_msg = ['ERROR:root:frozenset test is not a valid identifier!']
        err_msg = 'frozenset test is not a valid identifier!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(IdentifierError) as err:
                _ = Identifier(inp, 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_unnamed_deque(self):
        inp = deque([1, 2])
        log_msg = ['ERROR:root:deque([1, 2]) is not a valid identifier!']
        err_msg = 'deque([1, 2]) is not a valid identifier!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(IdentifierError) as err:
                _ = Identifier(inp)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_deque(self):
        inp = deque([1, 2])
        log_msg = ['ERROR:root:deque test is not a valid identifier!']
        err_msg = 'deque test is not a valid identifier!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(IdentifierError) as err:
                _ = Identifier(inp, 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_unnamed_ordereddict(self):
        inp = OrderedDict({1: 'one', 2: 'two'})
        log_msg = ["ERROR:root:OrderedDict([(1, 'one'), (2, 'two')])"
                   " is not a valid identifier!"]
        err_msg = ("OrderedDict([(1, 'one'), (2, 'two')])"
                   " is not a valid identifier!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(IdentifierError) as err:
                _ = Identifier(inp)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_ordereddict(self):
        inp = OrderedDict({1: 'one', 2: 'two'})
        log_msg = ['ERROR:root:OrderedDict test is not a valid identifier!']
        err_msg = 'OrderedDict test is not a valid identifier!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(IdentifierError) as err:
                _ = Identifier(inp, 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_unnamed_defaultdict(self):
        inp = defaultdict(str, {1: 'one', 2: 'two'})
        log_msg = ["ERROR:root:defaultdict(<class 'str'>, "
                   "{1: 'one', 2: 'two'}) is not a valid identifier!"]
        err_msg = ("defaultdict(<class 'str'>, "
                   "{1: 'one', 2: 'two'}) is not a valid identifier!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(IdentifierError) as err:
                _ = Identifier(inp)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_defaultdict(self):
        inp = defaultdict(str, {1: 'one', 2: 'two'})
        log_msg = ['ERROR:root:defaultdict test is not a valid identifier!']
        err_msg = 'defaultdict test is not a valid identifier!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(IdentifierError) as err:
                _ = Identifier(inp, 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_unnamed_dict_keys(self):
        inp = {1: 'one', 2: 'two'}
        log_msg = ['ERROR:root:dict_keys([1, 2]) is not a valid identifier!']
        err_msg = 'dict_keys([1, 2]) is not a valid identifier!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(IdentifierError) as err:
                _ = Identifier(inp.keys())
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_dict_keys(self):
        inp = {1: 'one', 2: 'two'}
        log_msg = ['ERROR:root:dict_keys test is not a valid identifier!']
        err_msg = 'dict_keys test is not a valid identifier!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(IdentifierError) as err:
                _ = Identifier(inp.keys(), 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_unnamed_ordereddict_keys(self):
        inp = OrderedDict({1: 'one', 2: 'two'})
        log_msg = ['ERROR:root:odict_keys([1, 2]) is not a valid identifier!']
        err_msg = 'odict_keys([1, 2]) is not a valid identifier!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(IdentifierError) as err:
                _ = Identifier(inp.keys())
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_ordereddict_keys(self):
        inp = OrderedDict({1: 'one', 2: 'two'})
        log_msg = ['ERROR:root:odict_keys test is not a valid identifier!']
        err_msg = 'odict_keys test is not a valid identifier!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(IdentifierError) as err:
                _ = Identifier(inp.keys(), 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_unnamed_dict_values(self):
        inp = {'one': 1, 'two': 2}
        log_msg = ['ERROR:root:dict_values([1, 2]) is not a valid identifier!']
        err_msg = 'dict_values([1, 2]) is not a valid identifier!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(IdentifierError) as err:
                _ = Identifier(inp.values())
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_dict_values(self):
        inp = {'one': 1, 'two': 2}
        log_msg = ['ERROR:root:dict_values test is not a valid identifier!']
        err_msg = 'dict_values test is not a valid identifier!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(IdentifierError) as err:
                _ = Identifier(inp.values(), 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_unnamed_ordereddict_values(self):
        inp = OrderedDict({'one': 1, 'two': 2})
        log_msg = ['ERROR:root:odict_values([1, 2])'
                   ' is not a valid identifier!']
        err_msg = 'odict_values([1, 2]) is not a valid identifier!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(IdentifierError) as err:
                _ = Identifier(inp.values())
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_ordereddict_values(self):
        inp = OrderedDict({'one': 1, 'two': 2})
        log_msg = ['ERROR:root:odict_values test is not a valid identifier!']
        err_msg = 'odict_values test is not a valid identifier!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(IdentifierError) as err:
                _ = Identifier(inp.values(), 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_unnamed_dict_items(self):
        inp = {'one': 1, 'two': 2}
        log_msg = ["ERROR:root:dict_items([('one', 1), "
                   "('two', 2)]) is not a valid identifier!"]
        err_msg = ("dict_items([('one', 1), "
                   "('two', 2)]) is not a valid identifier!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(IdentifierError) as err:
                _ = Identifier(inp.items())
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_dict_items(self):
        inp = {'one': 1, 'two': 2}
        log_msg = ['ERROR:root:dict_items test is not a valid identifier!']
        err_msg = 'dict_items test is not a valid identifier!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(IdentifierError) as err:
                _ = Identifier(inp.items(), 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_unnamed_ordereddict_items(self):
        inp = OrderedDict({'one': 1, 'two': 2})
        log_msg = ["ERROR:root:odict_items([('one', 1), "
                   "('two', 2)]) is not a valid identifier!"]
        err_msg = ("odict_items([('one', 1), "
                   "('two', 2)]) is not a valid identifier!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(IdentifierError) as err:
                _ = Identifier(inp.items())
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_ordereddict_items(self):
        inp = OrderedDict({'one': 1, 'two': 2})
        log_msg = ['ERROR:root:odict_items test is not a valid identifier!']
        err_msg = 'odict_items test is not a valid identifier!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(IdentifierError) as err:
                _ = Identifier(inp.items(), 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)


class TestIdentifierMethods(ut.TestCase):

    def test_has_attribute_JustStr(self):
        self.assertTrue(hasattr(Identifier, 'JustStr'))

    def test_attribute_JustStr_is_CompositionOf(self):
        self.assertIsInstance(Identifier.JustStr, CompositionOf)

    def test_value_and_name_are_passed_through_JustStr(self):
        log_msg = ['ERROR:root:Value 1 of str test is not a valid identifier!']
        err_msg = 'Value 1 of str test is not a valid identifier!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(IdentifierError) as err:
                _ = Identifier.JustStr('1', 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_has_attribute_o(self):
        self.assertTrue(hasattr(Identifier, 'o'))

    def test_attribute_o_is_callable(self):
        self.assertTrue(callable(Identifier.o))

    def test_o_returns_composition(self):
        def f(x):
            return x
        composition = Identifier.o(f)
        self.assertIsInstance(composition, CompositionOf)

    def test_o_raises_error_on_argument_not_callable(self):
        err_msg = ('foo must be a callable that accepts (i) a value,'
                   ' (ii) an optional name for that value, and (iii)'
                   ' any number of keyword arguments!')
        with self.assertRaises(CallableError) as err:
            _ = Identifier.o('foo')
        self.assertEqual(str(err.exception), err_msg)


if __name__ == '__main__':
    ut.main()
