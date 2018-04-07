import logging
import unittest as ut
from collections import defaultdict, deque, OrderedDict
from ....functional import CompositionOf
from ....types.weak import Like
from ....exceptions import MissingAttrError, CallableError


class TestLikeInstantiation(ut.TestCase):

    def test_error_on_no_attrs_to_check(self):
        err_msg = 'Found no attributes to check for!'
        with self.assertRaises(AttributeError) as err:
            _ = Like()
        self.assertEqual(str(err.exception), err_msg)

    def test_works_with_one_valid_attribute(self):
        _ = Like('__init__')

    def test_works_with_one_valid_attribute_given_as_list(self):
        _ = Like(['__init__'], 1)

    def test_works_with_two_valid_attributes(self):
        _ = Like('__init__', '__new__')

    def test_works_with_two_valid_attributes_given_as_list(self):
        _ = Like(['__init__', '__new__'], 2)

    def test_error_on_one_attribute_not_identifier(self):
        err_msg = 'Attribute name 1 is not a valid identifier!'
        with self.assertRaises(ValueError) as err:
            _ = Like(1)
        self.assertEqual(str(err.exception), err_msg)

    def test_error_on_one_attribute_in_a_list_not_identifier(self):
        err_msg = 'Attribute name 1 is not a valid identifier!'
        with self.assertRaises(ValueError) as err:
            _ = Like([1])
        self.assertEqual(str(err.exception), err_msg)

    def test_error_on_one_of_two_attributes_not_identifier(self):
        err_msg = 'Attribute name 2 is not a valid identifier!'
        with self.assertRaises(ValueError) as err:
            _ = Like('__init__', 2)
        self.assertEqual(str(err.exception), err_msg)

    def test_error_on_one_of_two_attributes_in_a_list_not_identifier(self):
        err_msg = 'Attribute name 2 is not a valid identifier!'
        with self.assertRaises(ValueError) as err:
            _ = Like(['__init__', 2])
        self.assertEqual(str(err.exception), err_msg)

    def test_error_on_two_attributes_not_identifier(self):
        err_msg = 'Attribute name 1 is not a valid identifier!'
        with self.assertRaises(ValueError) as err:
            _ = Like(1, 2)
        self.assertEqual(str(err.exception), err_msg)

    def test_error_on_two_attributes_in_a_list_not_identifier(self):
        err_msg = 'Attribute name 1 is not a valid identifier!'
        with self.assertRaises(ValueError) as err:
            _ = Like([1, 2])
        self.assertEqual(str(err.exception), err_msg)

    def test_error_on_wrong_identifier(self):
        err_msg = 'Attribute-checker name @baz is not a valid identifier!'
        with self.assertRaises(ValueError) as err:
            _ = Like('__init__', identifier='@baz')
        self.assertEqual(str(err.exception), err_msg)

    def test_has_default_name(self):
        LikeInit = Like('__init__')
        self.assertEqual(LikeInit.__name__, 'Like')

    def test_identifier_sets_name_attribute(self):
        LikeInit = Like('__init__', identifier='LikeInit')
        self.assertEqual(LikeInit.__name__, 'LikeInit')

    def test_has_attribute_attrs_with_one_valid_attr(self):
        LikeInit = Like('__init__')
        self.assertTrue(hasattr(LikeInit, 'attrs'))

    def test_cannot_set_attribute_attrs(self):
        LikeInit = Like('__init__')
        with self.assertRaises(AttributeError):
            LikeInit.attrs = 'foo'

    def test_attribute_types_has_correct_value_with_one_valid_attr(self):
        LikeInit = Like('__init__')
        self.assertTupleEqual(LikeInit.attrs, ('__init__', ))

    def test_works_with_two_valid_attributes(self):
        _ = Like('__init__', '__new__')

    def test_has_attribute_attrs_with_two_valid_attributes(self):
        LikeInitNew = Like('__init__', '__new__')
        self.assertTrue(hasattr(LikeInitNew, 'attrs'))

    def test_attribute_types_has_correct_value_with_two_valid_attributes(self):
        LikeInitNew = Like('__init__', '__new__')
        self.assertTupleEqual(LikeInitNew.attrs, ('__init__', '__new__'))

    def test_works_with_attrs_given_as_tuple(self):
        LikeFooBar = Like(('foo', 'bar'))
        self.assertTupleEqual(LikeFooBar.attrs, ('foo', 'bar'))

    def test_works_with_attrs_given_as_list(self):
        LikeFooBar = Like(['foo', 'bar'])
        self.assertTupleEqual(LikeFooBar.attrs, ('foo', 'bar'))

    def test_works_with_attrs_given_as_deque(self):
        LikeFooBar = Like(deque(('foo', 'bar')))
        self.assertTupleEqual(LikeFooBar.attrs, ('foo', 'bar'))

    def test_works_with_attrs_given_as_set(self):
        LikeFooBar = Like({'foo', 'bar'})
        self.assertSetEqual(set(LikeFooBar.attrs), {'foo', 'bar'})

    def test_works_with_attrs_given_as_fozenset(self):
        LikeFooBar = Like(frozenset(('foo', 'bar')))
        self.assertSetEqual(set(LikeFooBar.attrs), {'foo', 'bar'})

    def test_works_with_attrs_given_as_dict(self):
        attrs = {'foo': 'foo', 'bar': 'bar'}
        LikeFooBar = Like(attrs)
        self.assertSetEqual(set(LikeFooBar.attrs), {'foo', 'bar'})

    def test_works_with_attrs_given_as_ordered_dict(self):
        attrs = OrderedDict({'foo': 'foo', 'bar': 'bar'})
        LikeFooBar = Like(attrs)
        self.assertSetEqual(set(LikeFooBar.attrs), {'foo', 'bar'})

    def test_works_with_attrs_given_as_defaultdict(self):
        attrs = defaultdict(str, {'foo': 'foo', 'bar': 'bar'})
        LikeFooBar = Like(attrs)
        self.assertSetEqual(set(LikeFooBar.attrs), {'foo', 'bar'})

    def test_works_with_attrs_given_as_dict_keys(self):
        attrs = {'foo': 'foo', 'bar': 'bar'}.keys()
        LikeFooBar = Like(attrs)
        self.assertSetEqual(set(LikeFooBar.attrs), {'foo', 'bar'})

    def test_works_with_attrs_given_as_ordered_dict_keys(self):
        attrs = OrderedDict({'foo': 'foo', 'bar': 'bar'}).keys()
        LikeFooBar = Like(attrs)
        self.assertSetEqual(set(LikeFooBar.attrs), {'foo', 'bar'})

    def test_works_with_attrs_given_as_defaultdict_keys(self):
        attrs = defaultdict(str, {'foo': 'foo', 'bar': 'bar'}).keys()
        LikeFooBar = Like(attrs)
        self.assertSetEqual(set(LikeFooBar.attrs), {'foo', 'bar'})

    def test_works_with_attrs_given_as_dict_values(self):
        attrs = {'foo': 'foo', 'bar': 'bar'}.values()
        LikeFooBar = Like(attrs)
        self.assertSetEqual(set(LikeFooBar.attrs), {'foo', 'bar'})

    def test_works_with_attrs_given_as_ordered_dict_values(self):
        attrs = OrderedDict({'foo': 'foo', 'bar': 'bar'}).values()
        LikeFooBar = Like(attrs)
        self.assertSetEqual(set(LikeFooBar.attrs), {'foo', 'bar'})

    def test_works_with_attrs_given_as_defaultdict_values(self):
        attrs = defaultdict(str, {'foo': 'foo', 'bar': 'bar'}).values()
        LikeFooBar = Like(attrs)
        self.assertSetEqual(set(LikeFooBar.attrs), {'foo', 'bar'})

    def test_non_str_attrs_given_after_iterable_are_ignored(self):
        LikeFooBar = Like(('foo', 'bar'), 1)
        self.assertTupleEqual(LikeFooBar.attrs, ('foo', 'bar'))

    def test_error_on_str_attr_given_after_iterable(self):
        err_msg = "Attribute name ('foo', 'bar') is not a valid identifier!"
        with self.assertRaises(ValueError) as err:
            _ = Like(('foo', 'bar'), 'egg')
        self.assertEqual(str(err.exception), err_msg)


class TestLike(ut.TestCase):

    def test_returns_correct_type_with_one_attr(self):
        LikeInit = Like('__init__')
        i = LikeInit(1)
        self.assertIsInstance(i, int)

    def test_returns_correct_value_with_one_attr(self):
        LikeInit = Like('__init__')
        self.assertEqual(LikeInit(2), 2)

    def test_returns_correct_type_with_two_attrs(self):
        LikeInitNew = Like('__init__', '__new__')
        i = LikeInitNew(3)
        self.assertIsInstance(i, int)

    def test_returns_correct_value_with_two_attrs(self):
        LikeInitNew = Like('__init__', '__new__')
        self.assertEqual(LikeInitNew(4), 4)

    def test_error_on_wrong_unnamed_variable_with_one_attr(self):
        LikeFoo = Like('foo')
        log_msg = ['ERROR:root:Object test of type str does'
                   ' not have required attribute foo!']
        err_msg = ('Object test of type str does not'
                   ' have required attribute foo!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(MissingAttrError) as err:
                _ = LikeFoo('test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_wrong_named_variable_with_one_attr(self):
        LikeFoo = Like('foo')
        log_msg = ['ERROR:root:Object integer of type int does'
                   ' not have required attribute foo!']
        err_msg = ('Object integer of type int does not'
                   ' have required attribute foo!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(MissingAttrError) as err:
                _ = LikeFoo(1, 'integer')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_wrong_unnamed_variable_with_two_attrs(self):
        LikeInitBar = Like('__init__', 'bar')
        log_msg = ['ERROR:root:Object test of type str does'
                   ' not have required attribute bar!']
        err_msg = ('Object test of type str does not'
                   ' have required attribute bar!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(MissingAttrError) as err:
                _ = LikeInitBar('test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_wrong_named_variable_with_two_attrs(self):
        LikeInitBar = Like('__init__', 'bar')
        log_msg = ['ERROR:root:Object integer of type int does'
                   ' not have required attribute bar!']
        err_msg = ('Object integer of type int does not'
                   ' have required attribute bar!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(MissingAttrError) as err:
                _ = LikeInitBar(2, 'integer')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)


class TestJustMethods(ut.TestCase):

    def test_has_attribute_o(self):
        LikeInit = Like('__init__')
        self.assertTrue(hasattr(LikeInit, 'o'))

    def test_attribute_o_is_callable(self):
        LikeInit = Like('__init__')
        self.assertTrue(callable(LikeInit.o))

    def test_o_returns_composition(self):
        LikeInit = Like('__init__')
        LikeInitnew = Like('__init__', '__new__')
        composition = LikeInit.o(LikeInitnew)
        self.assertIsInstance(composition, CompositionOf)

    def test_o_raises_error_on_argument_not_callable(self):
        LikeInit = Like('__init__')
        err_msg = ('foo must be a callable that accepts (i) a value,'
                   ' (ii) an optional name for that value, and (iii)'
                   ' any number of keyword arguments!')
        with self.assertRaises(CallableError) as err:
            _ = LikeInit.o('foo')
        self.assertEqual(str(err.exception), err_msg)


if __name__ == '__main__':
    ut.main()

