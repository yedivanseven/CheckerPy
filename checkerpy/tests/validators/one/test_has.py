import logging
import unittest as ut
from collections import deque, defaultdict, OrderedDict
from ....validators.one import Has
from ....exceptions import IdentifierError, MissingAttrError, CallableError
from ....functional import CompositionOf


class TestHasAttributeSpecification(ut.TestCase):

    def test_works_with_no_attr(self):
        inp = 'test'
        out = Has(inp)
        self.assertEqual(out, inp)

    def test_works_with_single_str_as_attr(self):
        inp = 'test'
        out = Has(inp, attr='__init__')
        self.assertEqual(out, inp)

    def test_error_on_single_attr_neither_str_nor_iterable(self):
        err_msg = ('Attribute specification 1 seems to '
                   'be neither str not iterable of str!')
        with self.assertRaises(IdentifierError) as err:
            _ = Has('test', attr=1)
        self.assertEqual(str(err.exception), err_msg)

    def test_error_on_attr_iterable_but_not_of_str(self):
        err_msg = 'Attribute name 1 is not a valid identifier!'
        with self.assertRaises(IdentifierError) as err:
            _ = Has('test', attr=(1, 2))
        self.assertEqual(str(err.exception), err_msg)

    def test_works_with_attrs_as_tuple(self):
        inp = 'test'
        out = Has(inp, attr=('__init__', '__len__'))
        self.assertEqual(out, inp)

    def test_works_with_attrs_as_list(self):
        inp = 'test'
        out = Has(inp, attr=['__init__', '__len__'])
        self.assertEqual(out, inp)

    def test_works_with_attrs_as_deque(self):
        inp = 'test'
        out = Has(inp, attr=deque(['__init__', '__len__']))
        self.assertEqual(out, inp)

    def test_works_with_attrs_as_set(self):
        inp = 'test'
        out = Has(inp, attr={'__init__', '__len__'})
        self.assertEqual(out, inp)

    def test_works_with_attrs_as_frozenset(self):
        inp = 'test'
        out = Has(inp, attr=frozenset({'__init__', '__len__'}))
        self.assertEqual(out, inp)

    def test_works_with_attrs_as_dict(self):
        inp = 'test'
        out = Has(inp, attr={'__init__': 1, '__len__': 2})
        self.assertEqual(out, inp)

    def test_works_with_attrs_as_ordered_dict(self):
        inp = 'test'
        out = Has(inp, attr=OrderedDict({'__init__': 1, '__len__': 2}))
        self.assertEqual(out, inp)

    def test_works_with_attrs_as_defaultdict(self):
        inp = 'test'
        out = Has(inp, attr=defaultdict(int, {'__init__': 1, '__len__': 2}))
        self.assertEqual(out, inp)

    def test_works_with_attrs_as_dict_keys(self):
        inp = 'test'
        out = Has(inp, attr={'__init__': 1, '__len__': 2}.keys())
        self.assertEqual(out, inp)

    def test_works_with_attrs_as_ordered_dict_keys(self):
        inp = 'test'
        out = Has(inp, attr=OrderedDict({'__init__': 1, '__len__': 2}).keys())
        self.assertEqual(out, inp)

    def test_works_with_attrs_as_defaultdict_keys(self):
        inp = 'test'
        attrs = defaultdict(int, {'__init__': 1, '__len__': 2}).keys()
        out = Has(inp, attr=attrs)
        self.assertEqual(out, inp)

    def test_works_with_attrs_as_dict_values(self):
        inp = 'test'
        out = Has(inp, attr={1: '__init__', 2: '__len__'}.values())
        self.assertEqual(out, inp)

    def test_works_with_attrs_as_ordered_dict_values(self):
        inp = 'test'
        attrs = OrderedDict({1: '__init__', 2: '__len__'}).values()
        out = Has(inp, attr=attrs)
        self.assertEqual(out, inp)

    def test_works_with_attrs_as_defaultdict_values(self):
        inp = 'test'
        attrs = defaultdict(str, {1: '__init__', 2: '__len__'}).values()
        out = Has(inp, attr=attrs)
        self.assertEqual(out, inp)


class TestHas(ut.TestCase):

    def test_error_unnamed_object_one_attr(self):
        log_msg = ['ERROR:root:Object [1, 2, 3] of type list'
                   ' does not have required attribute test!']
        err_msg = ('Object [1, 2, 3] of type list does'
                   ' not have required attribute test!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(MissingAttrError) as err:
                _ = Has([1, 2, 3], attr='test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_named_object_one_attr(self):
        log_msg = ['ERROR:root:Object foo of type list'
                   ' does not have required attribute test!']
        err_msg = ('Object foo of type list does'
                   ' not have required attribute test!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(MissingAttrError) as err:
                _ = Has([1, 2, 3], 'foo', attr='test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_unnamed_object_two_attrs(self):
        log_msg = ['ERROR:root:Object [1, 2, 3] of type list'
                   ' does not have required attribute test!']
        err_msg = ('Object [1, 2, 3] of type list does'
                   ' not have required attribute test!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(MissingAttrError) as err:
                _ = Has([1, 2, 3], attr=('test', 'bar'))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_named_object_two_attrs(self):
        log_msg = ['ERROR:root:Object foo of type list'
                   ' does not have required attribute test!']
        err_msg = ('Object foo of type list does'
                   ' not have required attribute test!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(MissingAttrError) as err:
                _ = Has([1, 2, 3], 'foo', attr=('test', 'bar'))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_unnamed_deque_one_attr(self):
        log_msg = ['ERROR:root:Object deque([1, 2, 3])'
                   ' does not have required attribute test!']
        err_msg = ('Object deque([1, 2, 3]) does'
                   ' not have required attribute test!')
        inp = deque([1, 2, 3])
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(MissingAttrError) as err:
                _ = Has(inp, attr='test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_named_deque_one_attr(self):
        log_msg = ['ERROR:root:Object foo of type deque'
                   ' does not have required attribute test!']
        err_msg = ('Object foo of type deque does'
                   ' not have required attribute test!')
        inp = deque([1, 2, 3])
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(MissingAttrError) as err:
                _ = Has(inp, 'foo', attr='test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_unnamed_frozenset_one_attr(self):
        log_msg = ['ERROR:root:Object frozenset({1, 2, 3})'
                   ' does not have required attribute test!']
        err_msg = ('Object frozenset({1, 2, 3}) does'
                   ' not have required attribute test!')
        inp = frozenset({1, 2, 3})
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(MissingAttrError) as err:
                _ = Has(inp, attr='test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_named_frozenset_one_attr(self):
        log_msg = ['ERROR:root:Object foo of type frozenset'
                   ' does not have required attribute test!']
        err_msg = ('Object foo of type frozenset does'
                   ' not have required attribute test!')
        inp = frozenset({1, 2, 3})
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(MissingAttrError) as err:
                _ = Has(inp, 'foo', attr='test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_unnamed_ordereddict_one_attr(self):
        log_msg = ["ERROR:root:Object OrderedDict([(1, 'one'), (2, 'two')])"
                   " does not have required attribute test!"]
        err_msg = ("Object OrderedDict([(1, 'one'), (2, 'two')])"
                   " does not have required attribute test!")
        inp = OrderedDict({1: 'one', 2: 'two'})
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(MissingAttrError) as err:
                _ = Has(inp, attr='test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_named_ordereddict_one_attr(self):
        log_msg = ['ERROR:root:Object foo of type OrderedDict'
                   ' does not have required attribute test!']
        err_msg = ('Object foo of type OrderedDict does'
                   ' not have required attribute test!')
        inp = OrderedDict({1: 'one', 2: 'two'})
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(MissingAttrError) as err:
                _ = Has(inp, 'foo', attr='test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_unnamed_defaultdict_one_attr(self):
        log_msg = ["ERROR:root:Object defaultdict(<class 'str'>, {1: 'one',"
                   " 2: 'two'}) does not have required attribute test!"]
        err_msg = ("Object defaultdict(<class 'str'>, {1: 'one',"
                   " 2: 'two'}) does not have required attribute test!")
        inp = defaultdict(str, {1: 'one', 2: 'two'})
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(MissingAttrError) as err:
                _ = Has(inp, attr='test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_named_defaultdict_one_attr(self):
        log_msg = ['ERROR:root:Object foo of type defaultdict'
                   ' does not have required attribute test!']
        err_msg = ('Object foo of type defaultdict does'
                   ' not have required attribute test!')
        inp = defaultdict(str, {1: 'one', 2: 'two'})
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(MissingAttrError) as err:
                _ = Has(inp, 'foo', attr='test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_unnamed_dict_keys_one_attr(self):
        log_msg = ['ERROR:root:Object dict_keys([1, 2]) '
                   'does not have required attribute test!']
        err_msg = ('Object dict_keys([1, 2]) does not'
                   ' have required attribute test!')
        inp = {1: 'one', 2: 'two'}.keys()
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(MissingAttrError) as err:
                _ = Has(inp, attr='test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_named_dict_keys_one_attr(self):
        log_msg = ['ERROR:root:Object foo of type dict_keys '
                   'does not have required attribute test!']
        err_msg = ('Object foo of type dict_keys does not'
                   ' have required attribute test!')
        inp = {1: 'one', 2: 'two'}.keys()
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(MissingAttrError) as err:
                _ = Has(inp, 'foo', attr='test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_unnamed_ordereddict_keys_one_attr(self):
        log_msg = ['ERROR:root:Object odict_keys([1, 2]) '
                   'does not have required attribute test!']
        err_msg = ('Object odict_keys([1, 2]) does not'
                   ' have required attribute test!')
        inp = OrderedDict({1: 'one', 2: 'two'}).keys()
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(MissingAttrError) as err:
                _ = Has(inp, attr='test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_named_ordereddict_keys_one_attr(self):
        log_msg = ['ERROR:root:Object foo of type odict_keys '
                   'does not have required attribute test!']
        err_msg = ('Object foo of type odict_keys does not'
                   ' have required attribute test!')
        inp = OrderedDict({1: 'one', 2: 'two'}).keys()
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(MissingAttrError) as err:
                _ = Has(inp, 'foo', attr='test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_unnamed_dict_values_one_attr(self):
        log_msg = ['ERROR:root:Object dict_values([1, 2]) '
                   'does not have required attribute test!']
        err_msg = ('Object dict_values([1, 2]) does not'
                   ' have required attribute test!')
        inp = {'one': 1, 'two': 2}.values()
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(MissingAttrError) as err:
                _ = Has(inp, attr='test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_named_dict_values_one_attr(self):
        log_msg = ['ERROR:root:Object foo of type dict_values '
                   'does not have required attribute test!']
        err_msg = ('Object foo of type dict_values does not'
                   ' have required attribute test!')
        inp = {'one': 1, 'two': 2}.values()
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(MissingAttrError) as err:
                _ = Has(inp, 'foo', attr='test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_unnamed_ordereddict_values_one_attr(self):
        log_msg = ['ERROR:root:Object odict_values([1, 2]) '
                   'does not have required attribute test!']
        err_msg = ('Object odict_values([1, 2]) does not'
                   ' have required attribute test!')
        inp = OrderedDict({'one': 1, 'two': 2}).values()
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(MissingAttrError) as err:
                _ = Has(inp, attr='test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_named_ordereddict_values_one_attr(self):
        log_msg = ['ERROR:root:Object foo of type odict_values '
                   'does not have required attribute test!']
        err_msg = ('Object foo of type odict_values does not'
                   ' have required attribute test!')
        inp = OrderedDict({'one': 1, 'two': 2}).values()
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(MissingAttrError) as err:
                _ = Has(inp, 'foo', attr='test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_unnamed_dict_items_one_attr(self):
        log_msg = ["ERROR:root:Object dict_items([('one', 1), ('two', 2)])"
                   " does not have required attribute test!"]
        err_msg = ("Object dict_items([('one', 1), ('two', 2)])"
                   " does not have required attribute test!")
        inp = {'one': 1, 'two': 2}.items()
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(MissingAttrError) as err:
                _ = Has(inp, attr='test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_named_dict_items_one_attr(self):
        log_msg = ["ERROR:root:Object foo of type dict_items"
                   " does not have required attribute test!"]
        err_msg = ("Object foo of type dict_items"
                   " does not have required attribute test!")
        inp = {'one': 1, 'two': 2}.items()
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(MissingAttrError) as err:
                _ = Has(inp, 'foo', attr='test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_unnamed_ordereddict_items_one_attr(self):
        log_msg = ["ERROR:root:Object odict_items([('one', 1), ('two', 2)])"
                   " does not have required attribute test!"]
        err_msg = ("Object odict_items([('one', 1), ('two', 2)])"
                   " does not have required attribute test!")
        inp = OrderedDict({'one': 1, 'two': 2}).items()
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(MissingAttrError) as err:
                _ = Has(inp, attr='test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_named_ordereddict_items_one_attr(self):
        log_msg = ["ERROR:root:Object foo of type odict_items"
                   " does not have required attribute test!"]
        err_msg = ("Object foo of type odict_items"
                   " does not have required attribute test!")
        inp = OrderedDict({'one': 1, 'two': 2}).items()
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(MissingAttrError) as err:
                _ = Has(inp, 'foo', attr='test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)


class TestHasMethods(ut.TestCase):

    def test_has_attribute_o(self):
        self.assertTrue(hasattr(Has, 'o'))

    def test_attribute_o_is_callable(self):
        self.assertTrue(callable(Has.o))

    def test_o_returns_composition(self):
        def f(x):
            return x
        composition = Has.o(f)
        self.assertIsInstance(composition, CompositionOf)

    def test_o_raises_error_on_argument_not_callable(self):
        err_msg = ('foo must be a callable that accepts (i) a value,'
                   ' (ii) an optional name for that value, and (iii)'
                   ' any number of keyword arguments!')
        with self.assertRaises(CallableError) as err:
            _ = Has.o('foo')
        self.assertEqual(str(err.exception), err_msg)


if __name__ == '__main__':
    ut.main()
