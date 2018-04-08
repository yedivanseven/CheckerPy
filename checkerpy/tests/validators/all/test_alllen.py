import logging
import unittest as ut
from collections import deque, defaultdict, OrderedDict
from ....validators.all import AllLen
from ....exceptions import LenError, IterError, CallableError
from ....types.one import _REDUCED_ITER
from ....types.all import _ALL_ITERABLES
from ....types.weak import _LIKE_ITERABLES
from ....functional import CompositionOf


class TestAllLen(ut.TestCase):

    def test_error_on_unnamed_variable_not_iterable(self):
        log_msg = ['ERROR:root:Variable 1 with type int does not seem'
                   ' to be an iterable with elements to inspect!']
        err_msg = ('Variable 1 with type int does not seem to'
                   ' be an iterable with elements to inspect!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(IterError) as err:
                _ = AllLen(1, alen=1)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_variable_not_iterable(self):
        log_msg = ['ERROR:root:Variable test with type int does not '
                   'seem to be an iterable with elements to inspect!']
        err_msg = ('Variable test with type int does not seem '
                   'to be an iterable with elements to inspect!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(IterError) as err:
                _ = AllLen(1, 'test', alen=1)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_sane_tuple(self):
        inputs = ('foo', 'bar', 'baz')
        output = AllLen(inputs, alen=3)
        self.assertTupleEqual(output, inputs)

    def test_error_on_wrong_alen_element_in_unnamed_tuple(self):
        log_msg = ["ERROR:root:Length of str ba with index 1 in "
                   "tuple ('foo', 'ba', 'baz') must be 3, not 2!"]
        err_msg = ("Length of str ba with index 1 in tuple "
                   "('foo', 'ba', 'baz') must be 3, not 2!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = AllLen(('foo', 'ba', 'baz'), alen=3)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_wrong_alen_element_in_named_tuple(self):
        log_msg = ["ERROR:root:Length of str ba with index"
                   " 1 in tuple test must be 3, not 2!"]
        err_msg = ("Length of str ba with index 1 "
                   "in tuple test must be 3, not 2!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = AllLen(('foo', 'ba', 'baz'), 'test', alen=3)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_sane_list(self):
        inputs = ['foo', 'bar', 'baz']
        output = AllLen(inputs, alen=3)
        self.assertListEqual(output, inputs)

    def test_error_on_wrong_alen_element_in_unnamed_list(self):
        log_msg = ["ERROR:root:Length of str ba with index 1 in "
                   "list ['foo', 'ba', 'baz'] must be 3, not 2!"]
        err_msg = ("Length of str ba with index 1 in list "
                   "['foo', 'ba', 'baz'] must be 3, not 2!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = AllLen(['foo', 'ba', 'baz'], alen=3)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_wrong_alen_element_in_named_list(self):
        log_msg = ['ERROR:root:Length of str ba with index'
                   ' 1 in list test must be 3, not 2!']
        err_msg = ('Length of str ba with index 1 '
                   'in list test must be 3, not 2!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = AllLen(['foo', 'ba', 'baz'], 'test', alen=3)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_sane_deque(self):
        inputs = deque(['foo', 'bar', 'baz'])
        output = AllLen(inputs, alen=3)
        self.assertIsInstance(output, type(inputs))
        self.assertEqual(output, inputs)

    def test_error_on_wrong_alen_element_in_unnamed_deque(self):
        log_msg = ["ERROR:root:Length of str ba with index 1 in "
                   "deque(['foo', 'ba', 'baz']) must be 3, not 2!"]
        err_msg = ("Length of str ba with index 1 in deque"
                   "(['foo', 'ba', 'baz']) must be 3, not 2!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = AllLen(deque(['foo', 'ba', 'baz']), alen=3)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_wrong_alen_element_in_named_deque(self):
        log_msg = ['ERROR:root:Length of str ba with index'
                   ' 1 in deque test must be 3, not 2!']
        err_msg = ('Length of str ba with index 1 '
                   'in deque test must be 3, not 2!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = AllLen(deque(['foo', 'ba', 'baz']), 'test', alen=3)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_sane_set(self):
        inputs = {'foo', 'bar', 'baz'}
        output = AllLen(inputs, alen=3)
        self.assertSetEqual(output, inputs)

    def test_error_on_wrong_alen_element_in_unnamed_set(self):
        with self.assertLogs(level=logging.ERROR):
            with self.assertRaises(LenError):
                _ = AllLen({'foo', 'ba', 'baz'}, alen=3)

    def test_error_on_wrong_alen_element_in_named_set(self):
        log_msg = ['ERROR:root:Length of str ba in set test must be 3, not 2!']
        err_msg = 'Length of str ba in set test must be 3, not 2!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = AllLen({'foo', 'ba', 'baz'}, 'test', alen=3)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_sane_frozenset(self):
        inputs = frozenset({'foo', 'bar', 'baz'})
        output = AllLen(inputs, alen=3)
        self.assertSetEqual(output, inputs)

    def test_error_on_wrong_alen_element_in_unnamed_frozenset(self):
        with self.assertLogs(level=logging.ERROR):
            with self.assertRaises(LenError):
                _ = AllLen(frozenset({'foo', 'ba', 'baz'}), alen=3)

    def test_error_on_wrong_alen_element_in_named_frozenset(self):
        log_msg = ['ERROR:root:Length of str ba in '
                   'frozenset test must be 3, not 2!']
        err_msg = 'Length of str ba in frozenset test must be 3, not 2!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = AllLen(frozenset({'foo', 'ba', 'baz'}), 'test', alen=3)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_sane_dict(self):
        inputs = {'foo': 1, 'bar': 2, 'baz': 3}
        output = AllLen(inputs, alen=3)
        self.assertDictEqual(output, inputs)

    def test_error_on_wrong_alen_element_in_unnamed_dict(self):
        log_msg = ["ERROR:root:Length of str key ba in dict {'foo':"
                   " 1, 'ba': 2, 'baz': 3} must be 3, not 2!"]
        err_msg = ("Length of str key ba in dict {'foo': 1,"
                   " 'ba': 2, 'baz': 3} must be 3, not 2!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = AllLen({'foo': 1, 'ba': 2, 'baz': 3}, alen=3)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_wrong_alen_element_in_named_dict(self):
        log_msg = ['ERROR:root:Length of str key ba'
                   ' in dict test must be 3, not 2!']
        err_msg = 'Length of str key ba in dict test must be 3, not 2!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = AllLen({'foo': 1, 'ba': 2, 'baz': 3}, 'test', alen=3)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_sane_dict_keys(self):
        inputs = {'foo': 1, 'bar': 2, 'baz': 3}
        output = AllLen(inputs.keys(), alen=3)
        self.assertIsInstance(output, type(inputs.keys()))
        self.assertSetEqual(set(output), set(inputs.keys()))

    def test_error_on_wrong_alen_element_in_unnamed_dict_keys(self):
        inputs = {'foo': 1, 'ba': 2, 'baz': 3}
        log_msg = ["ERROR:root:Length of str key ba in dict_keys"
                   "(['foo', 'ba', 'baz']) must be 3, not 2!"]
        err_msg = ("Length of str key ba in dict_keys(['foo',"
                   " 'ba', 'baz']) must be 3, not 2!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = AllLen(inputs.keys(), alen=3)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_wrong_alen_element_in_named_dict_keys(self):
        inputs = {'foo': 1, 'ba': 2, 'baz': 3}
        log_msg = ['ERROR:root:Length of str key ba '
                   'in dict test must be 3, not 2!']
        err_msg = 'Length of str key ba in dict test must be 3, not 2!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = AllLen(inputs.keys(), 'test', alen=3)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_sane_dict_values(self):
        inputs = {1: 'foo', 2: 'bar', 3: 'baz'}
        output = AllLen(inputs.values(), alen=3)
        self.assertIsInstance(output, type(inputs.values()))
        self.assertSetEqual(set(output), set(inputs.values()))

    def test_error_on_wrong_alen_element_in_unnamed_dict_values(self):
        inputs = {1: 'foo', 2: 'ba', 3: 'baz'}
        log_msg = ["ERROR:root:Length of str value ba in dict_values"
                   "(['foo', 'ba', 'baz']) must be 3, not 2!"]
        err_msg = ("Length of str value ba in dict_values(['foo',"
                   " 'ba', 'baz']) must be 3, not 2!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = AllLen(inputs.values(), alen=3)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_wrong_alen_element_in_named_dict_values(self):
        inputs = {1: 'foo', 2: 'ba', 3: 'baz'}
        log_msg = ['ERROR:root:Length of str value ba'
                   ' in dict test must be 3, not 2!']
        err_msg = 'Length of str value ba in dict test must be 3, not 2!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = AllLen(inputs.values(), 'test', alen=3)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_sane_dict_items(self):
        inputs = {1: 'foo', 2: 'bar', 3: 'baz'}
        output = AllLen(inputs.items(), alen=2)
        self.assertIsInstance(output, type(inputs.items()))
        self.assertSetEqual(set(output), set(inputs.items()))

    def test_error_on_wrong_alen_element_in_unnamed_dict_items(self):
        inputs = {1: 'foo', 2: 'ba', 3: 'baz'}
        log_msg = ["ERROR:root:Length of tuple item (1, 'foo') in dict_items"
                   "([(1, 'foo'), (2, 'ba'), (3, 'baz')]) must be 3, not 2!"]
        err_msg = ("Length of tuple item (1, 'foo') in dict_items([(1, 'foo'),"
                   " (2, 'ba'), (3, 'baz')]) must be 3, not 2!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = AllLen(inputs.items(), alen=3)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_wrong_alen_element_in_named_dict_items(self):
        inputs = {1: 'foo', 2: 'ba', 3: 'baz'}
        log_msg = ["ERROR:root:Length of tuple item (1, 'foo')"
                   " in dict test must be 3, not 2!"]
        err_msg = ("Length of tuple item (1, 'foo') "
                   "in dict test must be 3, not 2!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = AllLen(inputs.items(), 'test', alen=3)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_sane_ordered_dict(self):
        inputs = OrderedDict({'foo': 1, 'bar': 2, 'baz': 3})
        output = AllLen(inputs, alen=3)
        self.assertDictEqual(output, inputs)

    def test_error_on_wrong_alen_element_in_unnamed_ordered_dict(self):
        inputs = OrderedDict({'foo': 1, 'ba': 2, 'baz': 3})
        log_msg = ["ERROR:root:Length of str key ba in OrderedDict([('foo',"
                   " 1), ('ba', 2), ('baz', 3)]) must be 3, not 2!"]
        err_msg = ("Length of str key ba in OrderedDict([('foo', 1),"
                   " ('ba', 2), ('baz', 3)]) must be 3, not 2!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = AllLen(inputs, alen=3)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_wrong_alen_element_in_unnamed_ordered_dict_keys(self):
        inputs = OrderedDict({'foo': 1, 'ba': 2, 'baz': 3}).keys()
        log_msg = ["ERROR:root:Length of str key ba in odict_keys"
                   "(['foo', 'ba', 'baz']) must be 3, not 2!"]
        err_msg = ("Length of str key ba in odict_keys"
                   "(['foo', 'ba', 'baz']) must be 3, not 2!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = AllLen(inputs, alen=3)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_wrong_alen_element_in_unnamed_ordered_dict_values(self):
        inputs = OrderedDict({1: 'foo', 2: 'ba', 3: 'baz'}).values()
        log_msg = ["ERROR:root:Length of str value ba in odict_values"
                   "(['foo', 'ba', 'baz']) must be 3, not 2!"]
        err_msg = ("Length of str value ba in odict_values(['foo',"
                   " 'ba', 'baz']) must be 3, not 2!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = AllLen(inputs, alen=3)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_wrong_alen_element_in_unnamed_ordered_dict_items(self):
        inputs = OrderedDict({1: 'foo', 2: 'ba', 3: 'baz'}).items()
        log_msg = ["ERROR:root:Length of tuple item (1, 'foo') in odict_items"
                   "([(1, 'foo'), (2, 'ba'), (3, 'baz')]) must be 3, not 2!"]
        err_msg = ("Length of tuple item (1, 'foo') in odict_items([(1,"
                   " 'foo'), (2, 'ba'), (3, 'baz')]) must be 3, not 2!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = AllLen(inputs, alen=3)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_wrong_alen_element_in_named_ordered_dict(self):
        inputs = OrderedDict({'foo': 1, 'ba': 2, 'baz': 3})
        log_msg = ['ERROR:root:Length of str key ba in '
                   'OrderedDict test must be 3, not 2!']
        err_msg = 'Length of str key ba in OrderedDict test must be 3, not 2!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = AllLen(inputs, 'test', alen=3)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_wrong_alen_element_in_named_ordered_dict_keys(self):
        inputs = OrderedDict({'foo': 1, 'ba': 2, 'baz': 3}).keys()
        log_msg = ["ERROR:root:Length of str key ba "
                   "in dict test must be 3, not 2!"]
        err_msg = "Length of str key ba in dict test must be 3, not 2!"
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = AllLen(inputs, 'test', alen=3)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_wrong_alen_element_in_named_ordered_dict_values(self):
        inputs = OrderedDict({1: 'foo', 2: 'ba', 3: 'baz'}).values()
        log_msg = ["ERROR:root:Length of str value ba"
                   " in dict test must be 3, not 2!"]
        err_msg = "Length of str value ba in dict test must be 3, not 2!"
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = AllLen(inputs, 'test', alen=3)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_wrong_alen_element_in_named_ordered_dict_items(self):
        inputs = OrderedDict({1: 'foo', 2: 'ba', 3: 'baz'}).items()
        log_msg = ["ERROR:root:Length of tuple item (1, "
                   "'foo') in dict test must be 3, not 2!"]
        err_msg = ("Length of tuple item (1, 'foo')"
                   " in dict test must be 3, not 2!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = AllLen(inputs, 'test', alen=3)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_sane_defaultdict(self):
        inputs = defaultdict(int, {'foo': 1, 'bar': 2, 'baz': 3})
        output = AllLen(inputs, alen=3)
        self.assertDictEqual(output, inputs)

    def test_error_on_wrong_alen_element_in_unnamed_defaultdict(self):
        inputs = defaultdict(int, {'foo': 1, 'ba': 2, 'baz': 3})
        log_msg = ["ERROR:root:Length of str key ba in defaultdict(<class "
                   "'int'>, {'foo': 1, 'ba': 2, 'baz': 3}) must be 3, not 2!"]
        err_msg = ("Length of str key ba in defaultdict(<class 'int'>, "
                   "{'foo': 1, 'ba': 2, 'baz': 3}) must be 3, not 2!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = AllLen(inputs, alen=3)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_wrong_alen_element_in_unnamed_defaultdict_keys(self):
        inputs = defaultdict(int, {'foo': 1, 'ba': 2, 'baz': 3})
        log_msg = ["ERROR:root:Length of str key ba in dict_keys"
                   "(['foo', 'ba', 'baz']) must be 3, not 2!"]
        err_msg = ("Length of str key ba in dict_keys(['foo',"
                   " 'ba', 'baz']) must be 3, not 2!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = AllLen(inputs.keys(), alen=3)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_wrong_alen_element_in_unnamed_defaultdict_values(self):
        inputs = defaultdict(str, {1: 'foo', 2: 'ba', 3: 'baz'})
        log_msg = ["ERROR:root:Length of str value ba in dict_values"
                   "(['foo', 'ba', 'baz']) must be 3, not 2!"]
        err_msg = ("Length of str value ba in dict_values(['foo',"
                   " 'ba', 'baz']) must be 3, not 2!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = AllLen(inputs.values(), alen=3)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_wrong_alen_element_in_unnamed_defaultdict_items(self):
        inputs = defaultdict(str, {1: 'foo', 2: 'ba', 3: 'baz'})
        log_msg = ["ERROR:root:Length of tuple item (1, 'foo') in dict_items"
                   "([(1, 'foo'), (2, 'ba'), (3, 'baz')]) must be 3, not 2!"]
        err_msg = ("Length of tuple item (1, 'foo') in dict_items([(1, 'foo'),"
                   " (2, 'ba'), (3, 'baz')]) must be 3, not 2!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = AllLen(inputs.items(), alen=3)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_wrong_alen_element_in_named_defaultdict(self):
        inputs = defaultdict(int, {'foo': 1, 'ba': 2, 'baz': 3})
        log_msg = ['ERROR:root:Length of str key ba in '
                   'defaultdict test must be 3, not 2!']
        err_msg = 'Length of str key ba in defaultdict test must be 3, not 2!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = AllLen(inputs, 'test', alen=3)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_wrong_alen_element_in_named_defaultdict_keys(self):
        inputs = defaultdict(str, {'foo': 1, 'ba': 2, 'baz': 3})
        log_msg = ['ERROR:root:Length of str key ba '
                   'in dict test must be 3, not 2!']
        err_msg = 'Length of str key ba in dict test must be 3, not 2!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = AllLen(inputs.keys(), 'test', alen=3)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_wrong_alen_element_in_named_defaultdict_values(self):
        inputs = defaultdict(str, {1: 'foo', 2: 'ba', 3: 'baz'})
        log_msg = ['ERROR:root:Length of str value ba'
                   ' in dict test must be 3, not 2!']
        err_msg = 'Length of str value ba in dict test must be 3, not 2!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = AllLen(inputs.values(), 'test', alen=3)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_wrong_alen_element_in_named_defaultdict_items(self):
        inputs = defaultdict(str, {1: 'foo', 2: 'ba', 3: 'baz'})
        log_msg = ["ERROR:root:Length of tuple item (1, 'foo')"
                   " in dict test must be 3, not 2!"]
        err_msg = ("Length of tuple item (1, 'foo') "
                   "in dict test must be 3, not 2!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = AllLen(inputs.items(), 'test', alen=3)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)


class TestAllLenMethods(ut.TestCase):

    def test_has_iterable_type_checker_attributes(self):
        for iterable in _REDUCED_ITER:
            self.assertTrue(hasattr(AllLen, iterable.__name__))
        for iterable in _LIKE_ITERABLES:
            self.assertTrue(hasattr(AllLen, iterable.__name__))

    def test_iterable_type_checkers_are_type_CompositionOf(self):
        for iterable in _REDUCED_ITER:
            type_checker = getattr(AllLen, iterable.__name__)
            self.assertIsInstance(type_checker, CompositionOf)
        for iterable in _LIKE_ITERABLES:
            type_checker = getattr(AllLen, iterable.__name__)
            self.assertIsInstance(type_checker, CompositionOf)

    def test_has_attribute_NonEmpty(self):
        self.assertTrue(hasattr(AllLen, 'NonEmpty'))

    def test_attribute_NonEmpty_is_type_CompositionOf(self):
        self.assertIsInstance(AllLen.NonEmpty, CompositionOf)

    def test_has_attribute_JustLen(self):
        self.assertTrue(hasattr(AllLen, 'JustLen'))

    def test_attribute_JustLen_is_type_CompositionOf(self):
        self.assertIsInstance(AllLen.JustLen, CompositionOf)

    def test_has_all_iterable_type_checker_attributes(self):
        for iterable in _ALL_ITERABLES:
            self.assertTrue(hasattr(AllLen, iterable.__name__))

    def test_all_iterable_type_checkers_are_type_CompositionOf(self):
        for iterable in _ALL_ITERABLES:
            type_checker = getattr(AllLen, iterable.__name__)
            self.assertIsInstance(type_checker, CompositionOf)

    def test_alen_is_passed_through_type_checker(self):
        log_msg = ['ERROR:root:Length of str ba with index'
                   ' 1 in tuple test must be 3, not 2!']
        err_msg = ('Length of str ba with index 1 '
                   'in tuple test must be 3, not 2!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = AllLen.AllStr(('foo', 'ba', 'baz'), 'test', alen=3)
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
