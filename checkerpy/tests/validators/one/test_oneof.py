import logging
import unittest as ut
from ....functional import CompositionOf
from ....validators.one import OneOf
from ....exceptions import ItemError, CallableError


class NoLenNoGetitem:
    def __init__(self, maximum):
        self.elements = [i for i in range(maximum)]

    def __contains__(self, value):
        return value in self.elements

    def __str__(self):
        return self.elements.__str__()


class GetItemNoLen:
    def __init__(self, maximum):
        self.elements = [i for i in range(maximum)]

    def __getitem__(self, index):
        return self.elements[index]

    def __str__(self):
        return self.elements.__str__()


class LenNoGetitem:
    def __init__(self, maximum):
        self.elements = [i for i in range(maximum)]

    def __len__(self):
        return len(self.elements)

    def __contains__(self, value):
        return value in self.elements

    def __str__(self):
        return self.elements.__str__()


class LenGetitem:
    def __init__(self, maximum):
        self.elements = [i for i in range(maximum)]

    def __len__(self):
        return len(self.elements)

    def __getitem__(self, index):
        return self.elements[index]

    def __str__(self):
        return self.elements.__str__()


class TestOneOfItems(ut.TestCase):

    def test_membership_error_on_item_not_container(self):
        log_msg = ['ERROR:root:Cannot determine if int 42 is one of 2!']
        err_msg = 'Cannot determine if int 42 is one of 2!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = OneOf(42, items=2)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_items_NoLenNoGetitem1(self):
        no_len_no_getitem_1 = NoLenNoGetitem(1)
        inputs = 0
        output = OneOf(inputs, items=no_len_no_getitem_1)
        self.assertEqual(output, inputs)

    def test_error_with_items_NoLenNoGetitem1(self):
        no_len_no_getitem_1 = NoLenNoGetitem(1)
        log_msg = ['ERROR:root:int 2 is not one of [0]!']
        err_msg = 'int 2 is not one of [0]!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = OneOf(2, items=no_len_no_getitem_1)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_items_NoLenNoGetitem3(self):
        no_len_no_getitem_3 = NoLenNoGetitem(3)
        inputs = 1
        output = OneOf(inputs, items=no_len_no_getitem_3)
        self.assertEqual(output, inputs)

    def test_error_with_items_NoLenNoGetitem3(self):
        no_len_no_getitem_3 = NoLenNoGetitem(3)
        log_msg = ['ERROR:root:int 3 is not one of [0, 1, 2]!']
        err_msg = 'int 3 is not one of [0, 1, 2]!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = OneOf(3, items=no_len_no_getitem_3)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_items_GetitemNoLen1(self):
        getitem_no_len_1 = GetItemNoLen(1)
        inputs = 0
        output = OneOf(inputs, items=getitem_no_len_1)
        self.assertEqual(output, inputs)

    def test_error_with_items_GetitemNoLen1(self):
        getitem_no_len_1 = GetItemNoLen(1)
        log_msg = ['ERROR:root:int 2 is not one of [0]!']
        err_msg = 'int 2 is not one of [0]!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = OneOf(2, items=getitem_no_len_1)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_items_GetitemNoLen3(self):
        getitem_no_len_3 = GetItemNoLen(3)
        inputs = 1
        output = OneOf(inputs, items=getitem_no_len_3)
        self.assertEqual(output, inputs)

    def test_error_with_items_GetitemNoLen3(self):
        getitem_no_len_3 = GetItemNoLen(3)
        log_msg = ['ERROR:root:int 3 is not one of [0, 1, 2]!']
        err_msg = 'int 3 is not one of [0, 1, 2]!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = OneOf(3, items=getitem_no_len_3)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_items_LenNoGetItem1(self):
        len_no_getitem_1 = LenNoGetitem(1)
        inputs = 0
        output = OneOf(inputs, items=len_no_getitem_1)
        self.assertEqual(output, inputs)

    def test_error_with_items_LenNoGetItem1(self):
        len_no_getitem_1 = LenNoGetitem(1)
        log_msg = ['ERROR:root:int 2 is not one of [0]!']
        err_msg = 'int 2 is not one of [0]!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = OneOf(2, items=len_no_getitem_1)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_items_LenNoGetItem3(self):
        len_no_getitem_3 = LenNoGetitem(3)
        inputs = 1
        output = OneOf(inputs, items=len_no_getitem_3)
        self.assertEqual(output, inputs)

    def test_error_with_items_LenNoGetItem3(self):
        len_no_getitem_3 = LenNoGetitem(3)
        log_msg = ['ERROR:root:int 3 is not one of [0, 1, 2]!']
        err_msg = 'int 3 is not one of [0, 1, 2]!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = OneOf(3, items=len_no_getitem_3)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_items_LenGetItem1(self):
        len_getitem_1 = LenGetitem(1)
        inputs = 0
        output = OneOf(inputs, items=len_getitem_1)
        self.assertEqual(output, inputs)

    def test_error_with_items_LenGetItem1(self):
        len_getitem_1 = LenGetitem(1)
        log_msg = ['ERROR:root:int 2 is not 0!']
        err_msg = 'int 2 is not 0!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = OneOf(2, items=len_getitem_1)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_items_LenGetItem3(self):
        len_getitem_3 = LenGetitem(3)
        inputs = 1
        output = OneOf(inputs, items=len_getitem_3)
        self.assertEqual(output, inputs)

    def test_error_with_items_LenGetItem3(self):
        len_getitem_3 = LenGetitem(3)
        log_msg = ['ERROR:root:int 3 is not one of [0, 1, 2]!']
        err_msg = 'int 3 is not one of [0, 1, 2]!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = OneOf(3, items=len_getitem_3)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)


class TestOneOfItemsAsDict(ut.TestCase):

    def test_works_with_items_dict_1(self):
        inputs = 1
        output = OneOf(inputs, items={1: 'one'})
        self.assertEqual(output, inputs)

    def test_works_with_items_dict_2(self):
        inputs = 1
        output = OneOf(inputs, items={1: 'one', 2: 'two'})
        self.assertEqual(output, inputs)

    def test_works_with_items_dictkeys_1(self):
        inputs = 1
        output = OneOf(inputs, items={1: 'one'}.keys())
        self.assertEqual(output, inputs)

    def test_works_with_items_dictkeys_2(self):
        inputs = 1
        output = OneOf(inputs, items={1: 'one', 2: 'two'}.keys())
        self.assertEqual(output, inputs)

    def test_works_with_items_dictvalues_1(self):
        inputs = 'one'
        output = OneOf(inputs, items={1: 'one'}.values())
        self.assertEqual(output, inputs)

    def test_works_with_items_dictvalues_2(self):
        inputs = 'one'
        output = OneOf(inputs, items={1: 'one', 2: 'two'}.values())
        self.assertEqual(output, inputs)

    def test_works_with_items_dictitems_1(self):
        inputs = (1, 'one')
        output = OneOf(inputs, items={1: 'one'}.items())
        self.assertTupleEqual(output, inputs)

    def test_works_with_items_dictitems_2(self):
        inputs = (1, 'one')
        output = OneOf(inputs, items={1: 'one', 2: 'two'}.items())
        self.assertTupleEqual(output, inputs)


class TestOneOfValue(ut.TestCase):

    def test_error_on_empty_items(self):
        log_msg = ['ERROR:root:int 1 is not one of ()!']
        err_msg = 'int 1 is not one of ()!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = OneOf(1, items=())
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_single_item(self):
        inputs = 2
        output = OneOf(inputs, items=(2,))
        self.assertIsInstance(output, type(inputs))
        self.assertEqual(output, inputs)

    def test_error_on_unnamed_value_single_item(self):
        log_msg = ['ERROR:root:int 1 is not 2!']
        err_msg = 'int 1 is not 2!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = OneOf(1, items=(2,))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_value_single_item(self):
        log_msg = ['ERROR:root:int test is not 2!']
        err_msg = 'int test is not 2!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = OneOf(1, 'test', items=(2,))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_multiple_items(self):
        inputs = 2
        output = OneOf(inputs, items=(2, 3))
        self.assertIsInstance(output, type(inputs))
        self.assertEqual(output, inputs)

    def test_error_on_unnamed_value_multiple_items(self):
        log_msg = ['ERROR:root:int 1 is not one of (2, 3)!']
        err_msg = 'int 1 is not one of (2, 3)!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = OneOf(1, items=(2, 3))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_value_multiple_items(self):
        log_msg = ['ERROR:root:int test is not one of (2, 3)!']
        err_msg = 'int test is not one of (2, 3)!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = OneOf(1, 'test', items=(2, 3))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_multiple_items_as_str(self):
        inputs = 'oo'
        items = 'foo'
        output = OneOf(inputs, items=items)
        self.assertIsInstance(output, type(inputs))
        self.assertEqual(output, inputs)

    def test_error_on_unnamed_value_item_as_str(self):
        log_msg = ['ERROR:root:str oo is not in str bar!']
        err_msg = 'str oo is not in str bar!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = OneOf('oo', items='bar')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_value_item_as_str(self):
        log_msg = ['ERROR:root:str test is not in str bar!']
        err_msg = 'str test is not in str bar!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = OneOf('oo', 'test', items='bar')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_item_tuple_of_empty_iterables(self):
        inputs = ()
        output = OneOf(inputs, items=((), [], {}))
        self.assertIsInstance(output, type(inputs))
        self.assertTupleEqual(output, inputs)

    def test_works_with_non_empty_tuple(self):
        inputs = (1, 2, 3)
        output = OneOf(inputs, items=[(1, 2, 3), 'foo', {'a': 4.0}])
        self.assertIsInstance(output, type(inputs))
        self.assertEqual(output, inputs)


class TestOneOfValueNamedTypes(ut.TestCase):

    def test_error_on_unamed_frozenset(self):
        inp = frozenset({1})
        log_msg = ['ERROR:root:frozenset({1}) is not 1!']
        err_msg = 'frozenset({1}) is not 1!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = OneOf(inp, items=[1])
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_amed_frozenset(self):
        inp = frozenset({1})
        log_msg = ['ERROR:root:frozenset test is not 1!']
        err_msg = 'frozenset test is not 1!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = OneOf(inp, 'test', items=[1])
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)


class TestOneOfIncomparable(ut.TestCase):

    def test_membership_error_named_value_incomparable(self):
        log_msg = ['ERROR:root:Cannot determine if int test is in str foo!']
        err_msg = 'Cannot determine if int test is in str foo!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = OneOf(42, 'test', items='foo')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_membership_error_unnamed_value_incomparable(self):
        log_msg = ['ERROR:root:Cannot determine if int 42 is in str foo!']
        err_msg = 'Cannot determine if int 42 is in str foo!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = OneOf(42, items='foo')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_membership_error_named_frozenset_incomparable(self):
        inp = frozenset({1})
        log_msg = ['ERROR:root:Cannot determine if '
                   'frozenset test is in str foo!']
        err_msg = 'Cannot determine if frozenset test is in str foo!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = OneOf(inp, 'test', items='foo')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_membership_error_unnamed_frozenset_incomparable(self):
        inp = frozenset({1})
        log_msg = ['ERROR:root:Cannot determine if '
                   'frozenset({1}) is in str foo!']
        err_msg = 'Cannot determine if frozenset({1}) is in str foo!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = OneOf(inp, items='foo')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)


class TestOneOfMethods(ut.TestCase):

    def test_has_attribute_o(self):
        self.assertTrue(hasattr(OneOf, 'o'))

    def test_attribute_o_is_callable(self):
        self.assertTrue(callable(OneOf.o))

    def test_o_returns_composition(self):
        def f(x):
            return x
        composition = OneOf.o(f)
        self.assertIsInstance(composition, CompositionOf)

    def test_o_raises_error_on_argument_not_callable(self):
        err_msg = ('foo must be a callable that accepts (i) a value,'
                   ' (ii) an optional name for that value, and (iii)'
                   ' any number of keyword arguments!')
        with self.assertRaises(CallableError) as err:
            _ = OneOf.o('foo')
        self.assertEqual(str(err.exception), err_msg)


if __name__ == '__main__':
    ut.main()
