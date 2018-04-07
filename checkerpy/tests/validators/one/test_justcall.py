import logging
import unittest as ut
from collections import defaultdict, deque, OrderedDict
from ....validators.one import JustCall
from ....exceptions import CallableError
from ....functional import CompositionOf


class TestJustCall(ut.TestCase):

    def test_works_with_sane_callable(self):
        inp = lambda x: x
        out = JustCall(inp)
        self.assertIs(out, inp)

    def test_error_on_unnamed_object_without_name_attr(self):
        log_msg = ['ERROR:root:Object foo of type str is not callable!']
        err_msg = 'Object foo of type str is not callable!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(CallableError) as err:
                _ = JustCall('foo')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_object_without_name_attr(self):
        log_msg = ['ERROR:root:Object test of type int is not callable!']
        err_msg = 'Object test of type int is not callable!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(CallableError) as err:
                _ = JustCall(1, 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_unnamed_object_with_name_attr(self):
        class Test:
            pass
        t = Test()
        t.__name__= 'test'
        log_msg = ['ERROR:root:Object test of type Test is not callable!']
        err_msg = 'Object test of type Test is not callable!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(CallableError) as err:
                _ = JustCall(t)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_object_with_name_attr(self):
        class Test:
            pass
        t = Test()
        t.__name__= 'test'
        log_msg = ['ERROR:root:Object name of type Test is not callable!']
        err_msg = 'Object name of type Test is not callable!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(CallableError) as err:
                _ = JustCall(t, 'name')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_with_unnamed_frozenset(self):
        inp = frozenset({1, 2})
        log_msg = ['ERROR:root:Object frozenset({1, 2}) is not callable!']
        err_msg = 'Object frozenset({1, 2}) is not callable!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(CallableError) as err:
                _ = JustCall(inp)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_with_named_frozenset(self):
        inp = frozenset({1, 2})
        log_msg = ['ERROR:root:Object test of type frozenset is not callable!']
        err_msg = 'Object test of type frozenset is not callable!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(CallableError) as err:
                _ = JustCall(inp, 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_with_unnamed_deque(self):
        inp = deque([1, 2])
        log_msg = ['ERROR:root:Object deque([1, 2]) is not callable!']
        err_msg = 'Object deque([1, 2]) is not callable!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(CallableError) as err:
                _ = JustCall(inp)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_with_named_deqeue(self):
        inp = deque([1, 2])
        log_msg = ['ERROR:root:Object test of type deque is not callable!']
        err_msg = 'Object test of type deque is not callable!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(CallableError) as err:
                _ = JustCall(inp, 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_with_unnamed_ordereddict(self):
        inp = OrderedDict({1: 'one', 2: 'two'})
        log_msg = ["ERROR:root:Object OrderedDict([(1, 'one'),"
                   " (2, 'two')]) is not callable!"]
        err_msg = ("Object OrderedDict([(1, 'one'),"
                   " (2, 'two')]) is not callable!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(CallableError) as err:
                _ = JustCall(inp)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_with_named_ordereddict(self):
        inp = OrderedDict({1: 'one', 2: 'two'})
        log_msg = ['ERROR:root:Object test of type'
                   ' OrderedDict is not callable!']
        err_msg = 'Object test of type OrderedDict is not callable!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(CallableError) as err:
                _ = JustCall(inp, 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_with_unnamed_defaultdict(self):
        inp = defaultdict(str, {1: 'one', 2: 'two'})
        log_msg = ["ERROR:root:Object defaultdict(<class 'str'>, "
                   "{1: 'one', 2: 'two'}) is not callable!"]
        err_msg = ("Object defaultdict(<class 'str'>, "
                   "{1: 'one', 2: 'two'}) is not callable!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(CallableError) as err:
                _ = JustCall(inp)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_with_named_defaultdict(self):
        inp = defaultdict(str, {1: 'one', 2: 'two'})
        log_msg = ['ERROR:root:Object test of type'
                   ' defaultdict is not callable!']
        err_msg = 'Object test of type defaultdict is not callable!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(CallableError) as err:
                _ = JustCall(inp, 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_with_unnamed_dict_keys(self):
        inp = {1: 'one', 2: 'two'}
        log_msg = ['ERROR:root:Object dict_keys([1, 2]) is not callable!']
        err_msg = 'Object dict_keys([1, 2]) is not callable!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(CallableError) as err:
                _ = JustCall(inp.keys())
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_with_named_dict_keys(self):
        inp = {1: 'one', 2: 'two'}
        log_msg = ['ERROR:root:Object test of type dict_keys is not callable!']
        err_msg = 'Object test of type dict_keys is not callable!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(CallableError) as err:
                _ = JustCall(inp.keys(), 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_with_unnamed_ordereddict_keys(self):
        inp = OrderedDict({1: 'one', 2: 'two'})
        log_msg = ['ERROR:root:Object odict_keys([1, 2]) is not callable!']
        err_msg = 'Object odict_keys([1, 2]) is not callable!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(CallableError) as err:
                _ = JustCall(inp.keys())
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_with_named_ordereddict_keys(self):
        inp = OrderedDict({1: 'one', 2: 'two'})
        log_msg = ['ERROR:root:Object test of type'
                   ' odict_keys is not callable!']
        err_msg = 'Object test of type odict_keys is not callable!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(CallableError) as err:
                _ = JustCall(inp.keys(), 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_with_unnamed_dict_values(self):
        inp = {'one': 1, 'two': 2}
        log_msg = ['ERROR:root:Object dict_values([1, 2]) is not callable!']
        err_msg = 'Object dict_values([1, 2]) is not callable!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(CallableError) as err:
                _ = JustCall(inp.values())
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_with_named_dict_values(self):
        inp = {'one': 1, 'two': 2}
        log_msg = ['ERROR:root:Object test of type'
                   ' dict_values is not callable!']
        err_msg = 'Object test of type dict_values is not callable!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(CallableError) as err:
                _ = JustCall(inp.values(), 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_with_unnamed_ordereddict_values(self):
        inp = OrderedDict({'one': 1, 'two': 2})
        log_msg = ['ERROR:root:Object odict_values([1, 2]) is not callable!']
        err_msg = 'Object odict_values([1, 2]) is not callable!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(CallableError) as err:
                _ = JustCall(inp.values())
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_with_named_ordereddict_values(self):
        inp = OrderedDict({'one': 1, 'two': 2})
        log_msg = ['ERROR:root:Object test of type'
                   ' odict_values is not callable!']
        err_msg = 'Object test of type odict_values is not callable!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(CallableError) as err:
                _ = JustCall(inp.values(), 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_with_unnamed_dict_items(self):
        inp = {'one': 1, 'two': 2}
        log_msg = ["ERROR:root:Object dict_items([('one', 1),"
                   " ('two', 2)]) is not callable!"]
        err_msg = ("Object dict_items([('one', 1),"
                   " ('two', 2)]) is not callable!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(CallableError) as err:
                _ = JustCall(inp.items())
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_with_named_dict_items(self):
        inp = {'one': 1, 'two': 2}
        log_msg = ['ERROR:root:Object test of type'
                   ' dict_items is not callable!']
        err_msg = 'Object test of type dict_items is not callable!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(CallableError) as err:
                _ = JustCall(inp.items(), 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_with_unnamed_ordereddict_items(self):
        inp = OrderedDict({'one': 1, 'two': 2})
        log_msg = ["ERROR:root:Object odict_items([('one', 1),"
                   " ('two', 2)]) is not callable!"]
        err_msg = ("Object odict_items([('one', 1),"
                   " ('two', 2)]) is not callable!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(CallableError) as err:
                _ = JustCall(inp.items())
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_with_named_ordereddict_items(self):
        inp = OrderedDict({'one': 1, 'two': 2})
        log_msg = ['ERROR:root:Object test of type'
                   ' odict_items is not callable!']
        err_msg = 'Object test of type odict_items is not callable!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(CallableError) as err:
                _ = JustCall(inp.items(), 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)


class TestJustCallMethods(ut.TestCase):

    def test_has_attribute_o(self):
        self.assertTrue(hasattr(JustCall, 'o'))

    def test_attribute_o_is_callable(self):
        self.assertTrue(callable(JustCall.o))

    def test_o_returns_composition(self):
        def f(x):
            return x
        composition = JustCall.o(f)
        self.assertIsInstance(composition, CompositionOf)

    def test_o_raises_error_on_argument_not_callable(self):
        err_msg = ('foo must be a callable that accepts (i) a value,'
                   ' (ii) an optional name for that value, and (iii)'
                   ' any number of keyword arguments!')
        with self.assertRaises(CallableError) as err:
            _ = JustCall.o('foo')
        self.assertEqual(str(err.exception), err_msg)


if __name__ == '__main__':
    ut.main()
