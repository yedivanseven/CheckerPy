import logging
import unittest as ut
from collections import deque, defaultdict, OrderedDict
from ....validators.all import AllHave
from ....exceptions import MissingAttrError, CallableError, IterError
from ....types.one import _REDUCED_ITER
from ....types.weak import _LIKE_ITERABLES
from ....functional import CompositionOf


class TestAllHave(ut.TestCase):

    def test_error_on_unnamed_variable_not_iterable(self):
        log_msg = ['ERROR:root:Variable 1 with type int does not seem'
                   ' to be an iterable with elements to inspect!']
        err_msg = ('Variable 1 with type int does not seem to'
                   ' be an iterable with elements to inspect!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(IterError) as err:
                _ = AllHave(1)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_variable_not_iterable(self):
        log_msg = ['ERROR:root:Variable test with type int does not '
                   'seem to be an iterable with elements to inspect!']
        err_msg = ('Variable test with type int does not seem '
                   'to be an iterable with elements to inspect!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(IterError) as err:
                _ = AllHave(1, 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_sane_tuple(self):
        inputs = (1, 2)
        output = AllHave(inputs)
        self.assertTupleEqual(output, inputs)

    def test_error_with_unnamed_tuple(self):
        log_msg = ['ERROR:root:Object 1 with index 0 in tuple (1, 2) '
                   'of type int does not have required attribute bar!']
        err_msg = ('Object 1 with index 0 in tuple (1, 2) of type int'
                   ' does not have required attribute bar!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(MissingAttrError) as err:
                _ = AllHave((1, 2), attrs='bar')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_with_named_tuple(self):
        log_msg = ['ERROR:root:Object 1 with index 0 in tuple foo '
                   'of type int does not have required attribute bar!']
        err_msg = ('Object 1 with index 0 in tuple foo of type int'
                   ' does not have required attribute bar!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(MissingAttrError) as err:
                _ = AllHave((1, 2), 'foo', attrs='bar')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_sane_list(self):
        inputs = [1, 2]
        output = AllHave(inputs)
        self.assertListEqual(output, inputs)

    def test_error_with_unnamed_list(self):
        log_msg = ['ERROR:root:Object 1 with index 0 in list [1, 2] '
                   'of type int does not have required attribute bar!']
        err_msg = ('Object 1 with index 0 in list [1, 2] of type int'
                   ' does not have required attribute bar!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(MissingAttrError) as err:
                _ = AllHave([1, 2], attrs='bar')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_with_named_list(self):
        log_msg = ['ERROR:root:Object 1 with index 0 in list foo '
                   'of type int does not have required attribute bar!']
        err_msg = ('Object 1 with index 0 in list foo of type int'
                   ' does not have required attribute bar!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(MissingAttrError) as err:
                _ = AllHave([1, 2], 'foo', attrs='bar')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_sane_deque(self):
        inputs = deque([1, 2])
        output = AllHave(inputs)
        self.assertIsInstance(output, type(inputs))
        self.assertEqual(output, inputs)

    def test_error_with_unnamed_deque(self):
        log_msg = ['ERROR:root:Object 1 with index 0 in deque([1, 2]) '
                   'of type int does not have required attribute bar!']
        err_msg = ('Object 1 with index 0 in deque([1, 2]) of type int'
                   ' does not have required attribute bar!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(MissingAttrError) as err:
                _ = AllHave(deque([1, 2]), attrs='bar')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_with_named_deque(self):
        log_msg = ['ERROR:root:Object 1 with index 0 in deque foo '
                   'of type int does not have required attribute bar!']
        err_msg = ('Object 1 with index 0 in deque foo of type int'
                   ' does not have required attribute bar!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(MissingAttrError) as err:
                _ = AllHave(deque([1, 2]), 'foo', attrs='bar')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_sane_set(self):
        inputs = {1, 2}
        output = AllHave(inputs)
        self.assertSetEqual(output, inputs)

    def test_error_with_unnamed_set(self):
        with self.assertLogs(level=logging.ERROR):
            with self.assertRaises(MissingAttrError):
                _ = AllHave({1, 2}, attrs='bar')

    def test_error_with_named_set(self):
        log_msg = ['ERROR:root:Object 1 in set foo '
                   'of type int does not have required attribute bar!']
        err_msg = ('Object 1 in set foo of type int'
                   ' does not have required attribute bar!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(MissingAttrError) as err:
                _ = AllHave({1, 2}, 'foo', attrs='bar')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_sane_frozenset(self):
        inputs = frozenset({1, 2})
        output = AllHave(inputs)
        self.assertSetEqual(output, inputs)

    def test_error_with_unnamed_frozenset(self):
        with self.assertLogs(level=logging.ERROR):
            with self.assertRaises(MissingAttrError):
                _ = AllHave(frozenset({1, 2}), attrs='bar')

    def test_error_with_named_frozenset(self):
        log_msg = ['ERROR:root:Object 1 in frozenset foo '
                   'of type int does not have required attribute bar!']
        err_msg = ('Object 1 in frozenset foo of type int'
                   ' does not have required attribute bar!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(MissingAttrError) as err:
                _ = AllHave(frozenset({1, 2}), 'foo', attrs='bar')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_sane_dict(self):
        inputs = {1: 1, 2: 2}
        output = AllHave(inputs)
        self.assertDictEqual(output, inputs)

    def test_error_with_unnamed_dict(self):
        log_msg = ['ERROR:root:Object 1 in keys to dict {1: 1, 2: 2} '
                   'of type int does not have required attribute bar!']
        err_msg = ('Object 1 in keys to dict {1: 1, 2: 2} of type int'
                   ' does not have required attribute bar!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(MissingAttrError) as err:
                _ = AllHave({1: 1, 2: 2}, attrs='bar')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_with_named_dict(self):
        log_msg = ['ERROR:root:Object 1 in keys to dict foo '
                   'of type int does not have required attribute bar!']
        err_msg = ('Object 1 in keys to dict foo of type int'
                   ' does not have required attribute bar!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(MissingAttrError) as err:
                _ = AllHave({1: 1, 2: 2}, 'foo', attrs='bar')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_sane_ordered_dict(self):
        inputs = OrderedDict({1: 1, 2: 2})
        output = AllHave(inputs)
        self.assertDictEqual(output, inputs)

    def test_error_with_unnamed_ordered_dict(self):
        log_msg = ['ERROR:root:Object 1 in keys to OrderedDict'
                   '([(1, 1), (2, 2)]) of type int does not '
                   'have required attribute bar!']
        err_msg = ('Object 1 in keys to OrderedDict([(1, 1), (2, 2)]) '
                   'of type int does not have required attribute bar!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(MissingAttrError) as err:
                _ = AllHave(OrderedDict({1: 1, 2: 2}), attrs='bar')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_with_named_ordered_dict(self):
        log_msg = ['ERROR:root:Object 1 in keys to OrderedDict foo '
                   'of type int does not have required attribute bar!']
        err_msg = ('Object 1 in keys to OrderedDict foo of type int'
                   ' does not have required attribute bar!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(MissingAttrError) as err:
                _ = AllHave(OrderedDict({1: 1, 2: 2}), 'foo', attrs='bar')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_sane_defaultdict(self):
        inputs = defaultdict(int, {1: 1, 2: 2})
        output = AllHave(inputs)
        self.assertDictEqual(output, inputs)

    def test_error_with_unnamed_defaultdict(self):
        with self.assertLogs(level=logging.ERROR) :
            with self.assertRaises(MissingAttrError):
                _ = AllHave(defaultdict(int, {1: 1, 2: 2}), attrs='bar')

    def test_error_with_named_defaultdict(self):
        log_msg = ['ERROR:root:Object 1 in keys to defaultdict foo '
                   'of type int does not have required attribute bar!']
        err_msg = ('Object 1 in keys to defaultdict foo of type int'
                   ' does not have required attribute bar!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(MissingAttrError) as err:
                _ = AllHave(defaultdict(int, {1: 1, 2: 2}), 'foo', attrs='bar')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_sane_dict_keys(self):
        inputs = {1: 1, 2: 2}.keys()
        output = AllHave(inputs)
        self.assertIsInstance(output, type(inputs))
        self.assertEqual(output, inputs)

    def test_error_with_unnamed_dict_keys(self):
        inputs = {1: 1, 2: 2}.keys()
        log_msg = ['ERROR:root:Object 1 in dict_keys([1, 2]) '
                   'of type int does not have required attribute bar!']
        err_msg = ('Object 1 in dict_keys([1, 2]) of type int'
                   ' does not have required attribute bar!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(MissingAttrError) as err:
                _ = AllHave(inputs, attrs='bar')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_with_named_dict_keys(self):
        inputs = {1: 1, 2: 2}.keys()
        log_msg = ['ERROR:root:Object 1 in dict_keys foo '
                   'of type int does not have required attribute bar!']
        err_msg = ('Object 1 in dict_keys foo of type int'
                   ' does not have required attribute bar!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(MissingAttrError) as err:
                _ = AllHave(inputs, 'foo', attrs='bar')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_sane_ordered_dict_keys(self):
        inputs = OrderedDict({1: 1, 2: 2}).keys()
        output = AllHave(inputs)
        self.assertIsInstance(output, type(inputs))
        self.assertEqual(output, inputs)

    def test_error_with_unnamed_ordered_dict_keys(self):
        inputs = OrderedDict({1: 1, 2: 2}).keys()
        log_msg = ['ERROR:root:Object 1 in odict_keys([1, 2]) '
                   'of type int does not have required attribute bar!']
        err_msg = ('Object 1 in odict_keys([1, 2]) of type int'
                   ' does not have required attribute bar!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(MissingAttrError) as err:
                _ = AllHave(inputs, attrs='bar')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_with_named_ordered_dict_keys(self):
        inputs = OrderedDict({1: 1, 2: 2}).keys()
        log_msg = ['ERROR:root:Object 1 in odict_keys foo '
                   'of type int does not have required attribute bar!']
        err_msg = ('Object 1 in odict_keys foo of type int'
                   ' does not have required attribute bar!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(MissingAttrError) as err:
                _ = AllHave(inputs, 'foo', attrs='bar')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_sane_defaultdict_keys(self):
        inputs = defaultdict(int, {1: 1, 2: 2}).keys()
        output = AllHave(inputs)
        self.assertIsInstance(output, type(inputs))
        self.assertEqual(output, inputs)

    def test_error_with_unnamed_defaultdict_keys(self):
        inputs = defaultdict(int, {1: 1, 2: 2}).keys()
        with self.assertLogs(level=logging.ERROR):
            with self.assertRaises(MissingAttrError):
                _ = AllHave(inputs, attrs='bar')

    def test_error_with_named_defaultdict_keys(self):
        inputs = defaultdict(int, {1: 1, 2: 2}).keys()
        log_msg = ['ERROR:root:Object 1 in dict_keys foo '
                   'of type int does not have required attribute bar!']
        err_msg = ('Object 1 in dict_keys foo of type int'
                   ' does not have required attribute bar!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(MissingAttrError) as err:
                _ = AllHave(inputs, 'foo', attrs='bar')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_sane_dict_values(self):
        inputs = {1: 1, 2: 2}.values()
        output = AllHave(inputs)
        self.assertIsInstance(output, type(inputs))
        self.assertEqual(output, inputs)

    def test_error_with_unnamed_dict_values(self):
        inputs = {1: 1, 2: 2}.values()
        log_msg = ['ERROR:root:Object 1 in dict_values([1, 2]) '
                   'of type int does not have required attribute bar!']
        err_msg = ('Object 1 in dict_values([1, 2]) of type int'
                   ' does not have required attribute bar!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(MissingAttrError) as err:
                _ = AllHave(inputs, attrs='bar')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_with_named_dict_values(self):
        inputs = {1: 1, 2: 2}.values()
        log_msg = ['ERROR:root:Object 1 in dict_values foo '
                   'of type int does not have required attribute bar!']
        err_msg = ('Object 1 in dict_values foo of type int'
                   ' does not have required attribute bar!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(MissingAttrError) as err:
                _ = AllHave(inputs, 'foo', attrs='bar')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_sane_ordered_dict_values(self):
        inputs = OrderedDict({1: 1, 2: 2}).values()
        output = AllHave(inputs)
        self.assertIsInstance(output, type(inputs))
        self.assertEqual(output, inputs)

    def test_error_with_unnamed_ordered_dict_values(self):
        inputs = OrderedDict({1: 1, 2: 2}).values()
        log_msg = ['ERROR:root:Object 1 in odict_values([1, 2]) '
                   'of type int does not have required attribute bar!']
        err_msg = ('Object 1 in odict_values([1, 2]) of type int'
                   ' does not have required attribute bar!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(MissingAttrError) as err:
                _ = AllHave(inputs, attrs='bar')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_with_named_ordered_dict_values(self):
        inputs = OrderedDict({1: 1, 2: 2}).values()
        log_msg = ['ERROR:root:Object 1 in odict_values foo '
                   'of type int does not have required attribute bar!']
        err_msg = ('Object 1 in odict_values foo of type int'
                   ' does not have required attribute bar!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(MissingAttrError) as err:
                _ = AllHave(inputs, 'foo', attrs='bar')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_sane_defaultdict_values(self):
        inputs = defaultdict(int, {1: 1, 2: 2}).values()
        output = AllHave(inputs)
        self.assertIsInstance(output, type(inputs))
        self.assertEqual(output, inputs)

    def test_error_with_unnamed_defaultdict_values(self):
        inputs = defaultdict(int, {1: 1, 2: 2}).values()
        with self.assertLogs(level=logging.ERROR):
            with self.assertRaises(MissingAttrError):
                _ = AllHave(inputs, attrs='bar')

    def test_error_with_named_defaultdict_values(self):
        inputs = defaultdict(int, {1: 1, 2: 2}).values()
        log_msg = ['ERROR:root:Object 1 in dict_values foo '
                   'of type int does not have required attribute bar!']
        err_msg = ('Object 1 in dict_values foo of type int'
                   ' does not have required attribute bar!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(MissingAttrError) as err:
                _ = AllHave(inputs, 'foo', attrs='bar')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_sane_dict_items(self):
        inputs = {1: 1, 2: 2}.items()
        output = AllHave(inputs)
        self.assertIsInstance(output, type(inputs))
        self.assertEqual(output, inputs)

    def test_error_with_unnamed_dict_items(self):
        inputs = {1: 1, 2: 2}.items()
        log_msg = ['ERROR:root:Object (1, 1) in dict_items([(1, 1), (2, 2)])'
                   ' of type tuple does not have required attribute bar!']
        err_msg = ('Object (1, 1) in dict_items([(1, 1), (2, 2)]) of '
                   'type tuple does not have required attribute bar!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(MissingAttrError) as err:
                _ = AllHave(inputs, attrs='bar')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_with_named_dict_items(self):
        inputs = {1: 1, 2: 2}.items()
        log_msg = ['ERROR:root:Object (1, 1) in dict_items foo '
                   'of type tuple does not have required attribute bar!']
        err_msg = ('Object (1, 1) in dict_items foo of type tuple'
                   ' does not have required attribute bar!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(MissingAttrError) as err:
                _ = AllHave(inputs, 'foo', attrs='bar')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_sane_ordered_dict_items(self):
        inputs = OrderedDict({1: 1, 2: 2}).items()
        output = AllHave(inputs)
        self.assertIsInstance(output, type(inputs))
        self.assertEqual(output, inputs)

    def test_error_with_unnamed_ordered_dict_items(self):
        inputs = OrderedDict({1: 1, 2: 2}).items()
        log_msg = ['ERROR:root:Object (1, 1) in odict_items([(1, 1), (2, 2)])'
                   ' of type tuple does not have required attribute bar!']
        err_msg = ('Object (1, 1) in odict_items([(1, 1), (2, 2)])'
                   ' of type tuple does not have required attribute bar!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(MissingAttrError) as err:
                _ = AllHave(inputs, attrs='bar')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_with_named_ordered_dict_items(self):
        inputs = OrderedDict({1: 1, 2: 2}).items()
        log_msg = ['ERROR:root:Object (1, 1) in odict_items foo '
                   'of type tuple does not have required attribute bar!']
        err_msg = ('Object (1, 1) in odict_items foo of type tuple'
                   ' does not have required attribute bar!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(MissingAttrError) as err:
                _ = AllHave(inputs, 'foo', attrs='bar')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_sane_defaultdict_items(self):
        inputs = defaultdict(int, {1: 1, 2: 2}).items()
        output = AllHave(inputs)
        self.assertIsInstance(output, type(inputs))
        self.assertEqual(output, inputs)

    def test_error_with_unnamed_defaultdict_items(self):
        inputs = defaultdict(int, {1: 1, 2: 2}).items()
        with self.assertLogs(level=logging.ERROR):
            with self.assertRaises(MissingAttrError):
                _ = AllHave(inputs, attrs='bar')

    def test_error_with_named_defaultdict_items(self):
        inputs = defaultdict(int, {1: 1, 2: 2}).items()
        log_msg = ['ERROR:root:Object (1, 1) in dict_items foo '
                   'of type tuple does not have required attribute bar!']
        err_msg = ('Object (1, 1) in dict_items foo of type tuple'
                   ' does not have required attribute bar!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(MissingAttrError) as err:
                _ = AllHave(inputs, 'foo', attrs='bar')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)


class TestAllHaveMethods(ut.TestCase):

    def test_has_iterable_type_checker_attributes(self):
        for iterable in _REDUCED_ITER:
            self.assertTrue(hasattr(AllHave, iterable.__name__))
        for iterable in _LIKE_ITERABLES:
            self.assertTrue(hasattr(AllHave, iterable.__name__))

    def test_iterable_type_checkers_are_type_CompositionOf(self):
        for iterable in _REDUCED_ITER:
            type_checker = getattr(AllHave, iterable.__name__)
            self.assertIsInstance(type_checker, CompositionOf)
        for iterable in _LIKE_ITERABLES:
            type_checker = getattr(AllHave, iterable.__name__)
            self.assertIsInstance(type_checker, CompositionOf)

    def test_has_attribute_NonEmpty(self):
        self.assertTrue(hasattr(AllHave, 'NonEmpty'))

    def test_attribute_NonEmpty_is_type_CompositionOf(self):
        self.assertIsInstance(AllHave.NonEmpty, CompositionOf)

    def test_has_attribute_JustLen(self):
        self.assertTrue(hasattr(AllHave, 'JustLen'))

    def test_attribute_JustLen_is_type_CompositionOf(self):
        self.assertIsInstance(AllHave.JustLen, CompositionOf)

    def test_attrs_is_passed_through_attrs_checker(self):
        log_msg = ['ERROR:root:Object foo with index 0 in tuple bar '
                   'of type str does not have required attribute egg!']
        err_msg = ('Object foo with index 0 in tuple bar of type str '
                   'does not have required attribute egg!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(MissingAttrError) as err:
                _ = AllHave.JustTuple(('foo', ), 'bar', attrs='egg')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_has_attribute_o(self):
        self.assertTrue(hasattr(AllHave, 'o'))

    def test_attribute_o_is_callable(self):
        self.assertTrue(callable(AllHave.o))

    def test_o_returns_composition(self):
        def f(x):
            return x
        composition = AllHave.o(f)
        self.assertIsInstance(composition, CompositionOf)

    def test_o_raises_error_on_argument_not_callable(self):
        err_msg = ('foo must be a callable that accepts (i) a value,'
                   ' (ii) an optional name for that value, and (iii)'
                   ' any number of keyword arguments!')
        with self.assertRaises(CallableError) as err:
            _ = AllHave.o('foo')
        self.assertEqual(str(err.exception), err_msg)


if __name__ == '__main__':
    ut.main()
