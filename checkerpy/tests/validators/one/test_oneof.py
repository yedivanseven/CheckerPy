import logging
import unittest as ut
from ....functional import CompositionOf
from ....validators.one import OneOf
from ....exceptions import ItemError, CallableError


class TestNoInMethods:
    def __init__(self):
        self.elements = [i for i in range(1)]

    def __len__(self):
        return len(self.elements)

    def __str__(self):
        return self.elements.__str__()


class TestLenContains:
    def __init__(self):
        self.elements = [i for i in range(3)]

    def __len__(self):
        return len(self.elements)

    def __contains__(self, value):
        return value in self.elements

    def __str__(self):
        return self.elements.__str__()


class TestLenIter:
    def __init__(self):
        self.elements = [i for i in range(3)]

    def __len__(self):
        return len(self.elements)

    def __iter__(self):
        return iter(self.elements)

    def __str__(self):
        return self.elements.__str__()


class TestIterNoLen:
    def __init__(self):
        self.elements = [i for i in range(3)]

    def __iter__(self):
        return iter(self.elements)

    def __str__(self):
        return self.elements.__str__()


class TestContainsNoLen:
    def __init__(self):
        self.elements = [i for i in range(3)]

    def __contains__(self, value):
        return value in self.elements

    def __str__(self):
        return self.elements.__str__()


class TestOneOfItems(ut.TestCase):

    def test_works_with_items_len_and_contains(self):
        test_len_contains = TestLenContains()
        inputs = 2
        output = OneOf(inputs, items=test_len_contains)
        self.assertEqual(output, inputs)

    def test_error_on_unnamed_value_with_items_len_and_contains(self):
        test_len_contains = TestLenContains()
        log_msg = ['ERROR:root:Value 3 with type int is not one of [0, 1, 2]!']
        err_msg = 'Value 3 with type int is not one of [0, 1, 2]!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = OneOf(3, items=test_len_contains)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_value_with_items_len_and_contains(self):
        test_len_contains = TestLenContains()
        log_msg = ['ERROR:root:Value 3 of test with '
                   'type int is not one of [0, 1, 2]!']
        err_msg = 'Value 3 of test with type int is not one of [0, 1, 2]!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = OneOf(3, 'test', items=test_len_contains)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_items_len_and_iter(self):
        test_len_iter = TestLenIter()
        inputs = 2
        output = OneOf(inputs, items=test_len_iter)
        self.assertEqual(output, inputs)

    def test_error_on_unnamed_value_with_items_len_and_iter(self):
        test_len_iter = TestLenIter()
        log_msg = ['ERROR:root:Value 3 with type int is not one of [0, 1, 2]!']
        err_msg = 'Value 3 with type int is not one of [0, 1, 2]!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = OneOf(3, items=test_len_iter)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_value_with_items_len_and_iter(self):
        test_len_iter = TestLenIter()
        log_msg = ['ERROR:root:Value 3 of test with '
                   'type int is not one of [0, 1, 2]!']
        err_msg = 'Value 3 of test with type int is not one of [0, 1, 2]!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = OneOf(3, 'test', items=test_len_iter)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_items_iter_no_len(self):
        test_iter_no_len = TestIterNoLen()
        inputs = 2
        output = OneOf(inputs, items=test_iter_no_len)
        self.assertEqual(output, inputs)

    def test_error_on_items_iter_no_len(self):
        test_iter_no_len = TestIterNoLen()
        log_msg = ['ERROR:root:Value 3 with type int is not one of [0, 1, 2]!']
        err_msg = 'Value 3 with type int is not one of [0, 1, 2]!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = OneOf(3, items=test_iter_no_len)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_items_contains_no_len(self):
        test_contains_no_len = TestContainsNoLen()
        inputs = 2
        output = OneOf(inputs, items=test_contains_no_len)
        self.assertEqual(output, inputs)

    def test_error_on_items_contains_no_len(self):
        test_contains_no_len = TestContainsNoLen()
        log_msg = ['ERROR:root:Value 3 with type int is not one of [0, 1, 2]!']
        err_msg = 'Value 3 with type int is not one of [0, 1, 2]!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = OneOf(3, items=test_contains_no_len)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)


class TestOneOfValue(ut.TestCase):

    def test_error_on_empty_items(self):
        log_msg = ['ERROR:root:Value 1 with type int is not one of ()!']
        err_msg = 'Value 1 with type int is not one of ()!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = OneOf(1, items=())
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_single_item(self):
        inputs = 2
        output = OneOf(inputs, items=(2,))
        self.assertEqual(output, inputs)

    def test_error_on_unnamed_value_single_item(self):
        log_msg = ['ERROR:root:Value 1 with type int is not 2!']
        err_msg = 'Value 1 with type int is not 2!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = OneOf(1, items=(2,))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_value_single_item(self):
        log_msg = ['ERROR:root:Value 1 of test with type int is not 2!']
        err_msg = 'Value 1 of test with type int is not 2!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = OneOf(1, 'test', items=(2,))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_multiple_items(self):
        inputs = 2
        output = OneOf(inputs, items=(2, 3))
        self.assertEqual(output, inputs)

    def test_error_on_unnamed_value_multiple_items(self):
        log_msg = ['ERROR:root:Value 1 with type int is not one of (2, 3)!']
        err_msg = 'Value 1 with type int is not one of (2, 3)!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = OneOf(1, items=(2, 3))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_value_multiple_items(self):
        log_msg = ['ERROR:root:Value 1 of test with'
                   ' type int is not one of (2, 3)!']
        err_msg = 'Value 1 of test with type int is not one of (2, 3)!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = OneOf(1, 'test', items=(2, 3))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_multiple_items_as_str(self):
        inputs = 'oo'
        items = 'foo'
        output = OneOf(inputs, items=items)
        self.assertEqual(output, inputs)

    def test_error_on_unnamed_value_item_as_str(self):
        log_msg = ['ERROR:root:Value oo with type str is not in bar!']
        err_msg = 'Value oo with type str is not in bar!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = OneOf('oo', items='bar')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_value_item_as_str(self):
        log_msg = ['ERROR:root:Value oo of test with type str is not in bar!']
        err_msg = 'Value oo of test with type str is not in bar!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = OneOf('oo', 'test', items='bar')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_item_tuple_of_empty_iterables(self):
        inputs = ()
        output = OneOf(inputs, items=((), [], {}))
        self.assertTupleEqual(output, inputs)

    def test_works_with_non_empty_tuple(self):
        inputs = (1, 2, 3)
        output = OneOf(inputs, items=[(1, 2, 3), 'foo', {'a': 4.0}])
        self.assertEqual(output, inputs)

    def test_membership_error_named_value_incomparable(self):
        log_msg = ['ERROR:root:Cannot determine if value'
                   ' 42 of test with type int is in foo!']
        err_msg = ('Cannot determine if value 42 of'
                   ' test with type int is in foo!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = OneOf(42, 'test', items='foo')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_membership_error_unnamed_value_incomparable(self):
        log_msg = ['ERROR:root:Cannot determine if '
                   'value 42 with type int is in foo!']
        err_msg = 'Cannot determine if value 42 with type int is in foo!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = OneOf(42, items='foo')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_membership_error_named_value_item_wrong_type(self):
        log_msg = ['ERROR:root:Cannot determine if value'
                   ' 42 of test with type int is one of 2!']
        err_msg = ('Cannot determine if value 42 of'
                   ' test with type int is one of 2!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = OneOf(42, 'test', items=2)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_membership_error_unnamed_value_item_wrong_type(self):
        log_msg = ['ERROR:root:Cannot determine if '
                   'value 42 with type int is one of 2!']
        err_msg = 'Cannot determine if value 42 with type int is one of 2!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = OneOf(42, items=2)
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
