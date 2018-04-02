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

    def test_works_with_attrs_as_forzenset(self):
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
