import logging
import unittest as ut
from collections import deque, defaultdict, OrderedDict
from ....validators.one import Contains
from ....exceptions import ItemError, IterError, CallableError
from ....functional import CompositionOf
from ....types.one import _ITERABLES
from ....types.weak import _LIKE_ITERABLES, LikeContainer


class TestContainsParameterSpecification(ut.TestCase):

    def test_works_with_no_params(self):
        inp = 'test'
        out = Contains(inp)
        self.assertEqual(out, inp)

    def test_works_with_some_as_string(self):
        inp = 'test'
        out = Contains(inp, some='tabc')
        self.assertEqual(out, inp)
        self.assertIsInstance(out, type(inp))

    def test_works_with_some_as_tuple(self):
        inp = 'test'
        out = Contains(inp, some=('te', ))
        self.assertEqual(out, inp)
        self.assertIsInstance(out, type(inp))

    def test_works_with_every_as_tuple(self):
        inp = 'test'
        out = Contains(inp, every=('te', ))
        self.assertEqual(out, inp)
        self.assertIsInstance(out, type(inp))

    def test_works_with_every_as_string(self):
        inp = 'test'
        out = Contains(inp, every='ts')
        self.assertEqual(out, inp)
        self.assertIsInstance(out, type(inp))

    def test_works_with_some_and_every_as_tuples(self):
        inp = 'test'
        out = Contains(inp, some=('te', ), every=('st', ))
        self.assertEqual(out, inp)
        self.assertIsInstance(out, type(inp))

    def test_works_with_some_and_every_as_strings(self):
        inp = 'test'
        out = Contains(inp, some='abcde', every='ts')
        self.assertEqual(out, inp)
        self.assertIsInstance(out, type(inp))


class TestContainsGeneral(ut.TestCase):

    def test_error_on_unnamed_argument_not_an_iterable(self):
        log_msg = ['ERROR:root:Int 1 does not seem to be an '
                   'iterable whose content could be checked!']
        err_msg = ('Int 1 does not seem to be an iterable'
                   ' whose content could be checked!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(IterError) as err:
                _ = Contains(1, some=[1])
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_argument_not_an_iterable(self):
        log_msg = ['ERROR:root:Int test does not seem to be an '
                   'iterable whose content could be checked!']
        err_msg = ('Int test does not seem to be an iterable'
                   ' whose content could be checked!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(IterError) as err:
                _ = Contains(1, 'test', some=[1])
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_has_iterable_type_checker_attributes(self):
        for iterable in _ITERABLES:
            self.assertTrue(hasattr(Contains, iterable.__name__))
        for iterable in _LIKE_ITERABLES:
            self.assertTrue(hasattr(Contains, iterable.__name__))
        self.assertTrue(hasattr(Contains,'LikeContainer'))

    def test_iterable_type_checkers_are_type_CompositionOf(self):
        for iterable in _ITERABLES:
            type_checker = getattr(Contains, iterable.__name__)
            self.assertIsInstance(type_checker, CompositionOf)
        for iterable in _LIKE_ITERABLES:
            type_checker = getattr(Contains, iterable.__name__)
            self.assertIsInstance(type_checker, CompositionOf)
        type_checker = getattr(Contains, 'LikeContainer')
        self.assertIsInstance(type_checker, CompositionOf)

    def test_some_is_passed_through_to_contains(self):
        err_msg = 'Int 5 is not in tuple (1, 2, 3)!'
        with self.assertRaises(ItemError) as err:
            _ = Contains.JustTuple((1, 2, 3), some=5, every=(2, 3))
        self.assertEqual(str(err.exception), err_msg)

    def test_every_is_passed_through_to_contains(self):
        err_msg = 'Int 5 is not in tuple (1, 2, 3)!'
        with self.assertRaises(ItemError) as err:
            _ = Contains.JustTuple((1, 2, 3), some=(3, 4), every=5)
        self.assertEqual(str(err.exception), err_msg)

    def test_has_attribute_o(self):
        self.assertTrue(hasattr(Contains, 'o'))

    def test_attribute_o_is_callable(self):
        self.assertTrue(callable(Contains.o))

    def test_o_returns_composition(self):
        def f(x):
            return x
        composition = Contains.o(f)
        self.assertIsInstance(composition, CompositionOf)

    def test_o_raises_error_on_argument_not_callable(self):
        err_msg = ('foo must be a callable that accepts (i) a value,'
                   ' (ii) an optional name for that value, and (iii)'
                   ' any number of keyword arguments!')
        with self.assertRaises(CallableError) as err:
            _ = Contains.o('foo')
        self.assertEqual(str(err.exception), err_msg)


class TestContainsIterables(ut.TestCase):

    def test_single_every_error_with_unnamed_tuple(self):
        log_msg = ['ERROR:root:Int 4 is not in tuple (1, 2, 3)!']
        err_msg = 'Int 4 is not in tuple (1, 2, 3)!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = Contains((1, 2, 3), every=[4])
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_multi_every_error_with_unnamed_list(self):
        log_msg = ['ERROR:root:Items (4, 5) are not in list [1, 2, 3]!']
        err_msg = 'Items (4, 5) are not in list [1, 2, 3]!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = Contains([1, 2, 3], every=[4, 5])
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_multi_every_error_with_unnamed_deque(self):
        log_msg = ['ERROR:root:Items (4, 5) are not in deque([1, 2, 3])!']
        err_msg = 'Items (4, 5) are not in deque([1, 2, 3])!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = Contains(deque([1, 2, 3]), every=[4, 5])
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_single_some_error_with_unnamed_set(self):
        log_msg = ['ERROR:root:Int 4 is not in set {1, 2, 3}!']
        err_msg = 'Int 4 is not in set {1, 2, 3}!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = Contains({1, 2, 3}, some=[4])
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_single_some_error_with_unnamed_frozenset(self):
        log_msg = ['ERROR:root:Int 4 is not in frozenset({1, 2, 3})!']
        err_msg = 'Int 4 is not in frozenset({1, 2, 3})!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = Contains(frozenset({1, 2, 3}), some=[4])
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_multi_some_error_with_unnamed_dict(self):
        log_msg = ["ERROR:root:None of [4, 5] are "
                   "in dict {1: 'one', 2: 'two'}!"]
        err_msg = "None of [4, 5] are in dict {1: 'one', 2: 'two'}!"
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = Contains({1: 'one', 2: 'two'}, some=[4, 5])
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_multi_some_error_with_unnamed_ordereddict(self):
        log_msg = ["ERROR:root:None of [4, 5] are in "
                   "OrderedDict([(1, 'one'), (2, 'two')])!"]
        err_msg = ("None of [4, 5] are in Ordered"
                   "Dict([(1, 'one'), (2, 'two')])!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = Contains(OrderedDict({1: 'one', 2: 'two'}), some=[4, 5])
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_single_some_error_with_unnamed_defaultdict(self):
        log_msg = ["ERROR:root:Int 4 is not in defaultdict"
                   "(<class 'str'>, {1: 'one', 2: 'two'})!"]
        err_msg = ("Int 4 is not in defaultdict"
                   "(<class 'str'>, {1: 'one', 2: 'two'})!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = Contains(defaultdict(str, {1: 'one', 2: 'two'}), some=[4])
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_multi_some_error_with_unnamed_dict_keys(self):
        log_msg = ['ERROR:root:None of [4, 5] are in dict_keys([1, 2])!']
        err_msg = 'None of [4, 5] are in dict_keys([1, 2])!'
        input = {1: 'one', 2: 'two'}
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = Contains(input.keys(), some=[4, 5])
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_multi_some_error_with_unnamed_ordereddict_keys(self):
        log_msg = ['ERROR:root:None of [4, 5] are in odict_keys([1, 2])!']
        err_msg = 'None of [4, 5] are in odict_keys([1, 2])!'
        inp = OrderedDict({1: 'one', 2: 'two'})
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = Contains(inp.keys(), some=[4, 5])
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_multi_some_error_with_unnamed_defaultdict_keys(self):
        log_msg = ['ERROR:root:None of [4, 5] are in dict_keys([1, 2])!']
        err_msg = 'None of [4, 5] are in dict_keys([1, 2])!'
        inp = defaultdict(str, {1: 'one', 2: 'two'})
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = Contains(inp.keys(), some=[4, 5])
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_multi_some_error_with_unnamed_dict_values(self):
        log_msg = ['ERROR:root:None of [4, 5] are in dict_values([1, 2])!']
        err_msg = 'None of [4, 5] are in dict_values([1, 2])!'
        inp = {'one': 1, 'two': 2}
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = Contains(inp.values(), some=[4, 5])
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_multi_some_error_with_unnamed_ordereddict_values(self):
        log_msg = ['ERROR:root:None of [4, 5] are in odict_values([1, 2])!']
        err_msg = 'None of [4, 5] are in odict_values([1, 2])!'
        inp = OrderedDict({'one': 1, 'two': 2})
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = Contains(inp.values(), some=[4, 5])
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_multi_some_error_with_unnamed_defaultdict_values(self):
        log_msg = ['ERROR:root:None of [4, 5] are in dict_values([1, 2])!']
        err_msg = 'None of [4, 5] are in dict_values([1, 2])!'
        inp = defaultdict(int, {'one': 1, 'two': 2})
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = Contains(inp.values(), some=[4, 5])
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_multi_some_error_with_unnamed_dict_items(self):
        log_msg = ["ERROR:root:None of [4, 5] are in "
                   "dict_items([('one', 1), ('two', 2)])!"]
        err_msg = "None of [4, 5] are in dict_items([('one', 1), ('two', 2)])!"
        inp = {'one': 1, 'two': 2}
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = Contains(inp.items(), some=[4, 5])
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_single_some_error_with_unnamed_ordereddict_items(self):
        log_msg = ["ERROR:root:Int 4 is not in odict_"
                   "items([('one', 1), ('two', 2)])!"]
        err_msg = "Int 4 is not in odict_items([('one', 1), ('two', 2)])!"
        inp = OrderedDict({'one': 1, 'two': 2})
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = Contains(inp.items(), some=[4])
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_multi_some_error_with_unnamed_defaultdict_items(self):
        log_msg = ["ERROR:root:None of [4, 5] are in "
                   "dict_items([('one', 1), ('two', 2)])!"]
        err_msg = "None of [4, 5] are in dict_items([('one', 1), ('two', 2)])!"
        inp = defaultdict(int, {'one': 1, 'two': 2})
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = Contains(inp.items(), some=[4, 5])
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_multi_every_error_with_named_tuple(self):
        log_msg = ['ERROR:root:Items (4, 5) are not in tuple test!']
        err_msg = 'Items (4, 5) are not in tuple test!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = Contains((1, 2, 3), 'test', every=[4, 5])
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_multi_every_error_with_named_list(self):
        log_msg = ['ERROR:root:Items (4, 5) are not in list test!']
        err_msg = 'Items (4, 5) are not in list test!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = Contains([1, 2, 3], 'test', every=[4, 5])
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_multi_some_error_with_named_deque(self):
        log_msg = ['ERROR:root:Items (4, 5) are not in deque test!']
        err_msg = 'Items (4, 5) are not in deque test!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = Contains(deque([1, 2, 3]), 'test', every=[4, 5])
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_multi_every_error_with_named_set(self):
        log_msg = ['ERROR:root:Items (4, 5) are not in set test!']
        err_msg = 'Items (4, 5) are not in set test!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = Contains({1, 2, 3}, 'test', every=[4, 5])
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_single_some_error_with_named_frozenset(self):
        log_msg = ['ERROR:root:Int 4 is not in frozenset test!']
        err_msg = 'Int 4 is not in frozenset test!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = Contains(frozenset({1, 2, 3}), 'test', some=[4])
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_multi_every_error_with_named_dict(self):
        log_msg = ['ERROR:root:Items (4, 5) are not in dict test!']
        err_msg = 'Items (4, 5) are not in dict test!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = Contains({1: 'one', 2: 'two'}, 'test', every=[4, 5])
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_multi_every_error_with_named_ordereddict(self):
        log_msg = ['ERROR:root:Items (4, 5) are not in OrderedDict test!']
        err_msg = 'Items (4, 5) are not in OrderedDict test!'
        inp = OrderedDict({1: 'one', 2: 'two'})
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = Contains(inp, 'test', every=[4, 5])
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_multi_some_error_with_named_defaultdict(self):
        log_msg = ['ERROR:root:None of [4, 5] are in defaultdict test!']
        err_msg = 'None of [4, 5] are in defaultdict test!'
        inp = defaultdict(str, {1: 'one', 2: 'two'})
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = Contains(inp, 'test', some=[4, 5])
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_multi_some_error_with_named_dict_keys(self):
        log_msg = ['ERROR:root:None of [4, 5] are in dict_keys test!']
        err_msg = 'None of [4, 5] are in dict_keys test!'
        inp = {1: 'one', 2: 'two'}
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = Contains(inp.keys(), 'test', some=[4, 5])
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_multi_some_error_with_named_ordereddict_keys(self):
        log_msg = ['ERROR:root:None of [4, 5] are in odict_keys test!']
        err_msg = 'None of [4, 5] are in odict_keys test!'
        inp = OrderedDict({1: 'one', 2: 'two'})
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = Contains(inp.keys(), 'test', some=[4, 5])
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_multi_some_error_with_named_defaultdict_keys(self):
        log_msg = ['ERROR:root:None of [4, 5] are in dict_keys test!']
        err_msg = 'None of [4, 5] are in dict_keys test!'
        inp = defaultdict(str, {1: 'one', 2: 'two'})
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = Contains(inp.keys(), 'test', some=[4, 5])
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_multi_some_error_with_named_dict_values(self):
        log_msg = ['ERROR:root:None of [4, 5] are in dict_values test!']
        err_msg = 'None of [4, 5] are in dict_values test!'
        inp = {1: 'one', 2: 'two'}
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = Contains(inp.values(), 'test', some=[4, 5])
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_multi_some_error_with_named_ordereddict_values(self):
        log_msg = ['ERROR:root:None of [4, 5] are in odict_values test!']
        err_msg = 'None of [4, 5] are in odict_values test!'
        inp = OrderedDict({1: 'one', 2: 'two'})
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = Contains(inp.values(), 'test', some=[4, 5])
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_multi_some_error_with_named_defaultdict_values(self):
        log_msg = ['ERROR:root:None of [4, 5] are in dict_values test!']
        err_msg = 'None of [4, 5] are in dict_values test!'
        inp = defaultdict(str, {1: 'one', 2: 'two'})
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = Contains(inp.values(), 'test', some=[4, 5])
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_multi_some_error_with_named_dict_items(self):
        log_msg = ['ERROR:root:None of [4, 5] are in dict_items test!']
        err_msg = 'None of [4, 5] are in dict_items test!'
        input = {1: 'one', 2: 'two'}
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = Contains(input.items(), 'test', some=[4, 5])
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_multi_some_error_with_named_ordereddict_items(self):
        log_msg = ['ERROR:root:None of [4, 5] are in odict_items test!']
        err_msg = 'None of [4, 5] are in odict_items test!'
        inp = OrderedDict({1: 'one', 2: 'two'})
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = Contains(inp.items(), 'test', some=[4, 5])
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_multi_some_error_with_named_defaultdict_items(self):
        log_msg = ['ERROR:root:None of [4, 5] are in dict_items test!']
        err_msg = 'None of [4, 5] are in dict_items test!'
        inp = defaultdict(str, {1: 'one', 2: 'two'})
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = Contains(inp.items(), 'test', some=[4, 5])
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)


if __name__ == '__main__':
    ut.main()
