import logging
import unittest as ut
from ....validators.one import OneOf
from ....exceptions import ItemError


class TestOneOf(ut.TestCase):

    def test_works_with_single_item(self):
        inputs = 2
        output = OneOf(inputs, items=2)
        self.assertEqual(output, inputs)

    def test_error_on_unnamed_value_single_item(self):
        log_msg = ['ERROR:root:Value 1 with type int is not 2!']
        err_msg = 'Value 1 with type int is not 2!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = OneOf(1, items=2)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_value_single_item(self):
        log_msg = ['ERROR:root:Value 1 of test with type int is not 2!']
        err_msg = 'Value 1 of test with type int is not 2!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = OneOf(1, 'test', items=2)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_multiple_items_as_tuple(self):
        inputs = 2
        output = OneOf(inputs, items=(2, 3))
        self.assertEqual(output, inputs)

    def test_works_with_multiple_items_as_list(self):
        inputs = 2
        output = OneOf(inputs, items=[2, 3])
        self.assertEqual(output, inputs)

    def test_works_with_multiple_items_as_set(self):
        inputs = 2
        output = OneOf(inputs, items={2, 3})
        self.assertEqual(output, inputs)

    def test_error_on_unnamed_value_multiple_items(self):
        log_msg = ['ERROR:root:Value 1 with type int is not one of (2, 3)!']
        err_msg = 'Value 1 with type int is not one of (2, 3)!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = OneOf(1, items=(2, 3))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_value_multiple_item(self):
        log_msg = ['ERROR:root:Value 1 of test with'
                   ' type int is not one of (2, 3)!']
        err_msg = 'Value 1 of test with type int is not one of (2, 3)!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = OneOf(1, 'test', items=(2, 3))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_empty_item_tuple(self):
        inputs = ()
        output = OneOf(inputs, items=())
        self.assertEqual(output, inputs)

    def test_works_with_empty_item_list(self):
        inputs = []
        output = OneOf(inputs, items=[])
        self.assertEqual(output, inputs)

    def test_works_with_empty_item_set(self):
        inputs = {}
        output = OneOf(inputs, items={})
        self.assertEqual(output, inputs)

    def test_works_with_item_tuple_of_empty_iterables(self):
        inputs = ()
        output = OneOf(inputs, items=((), [], {}))
        self.assertEqual(output, inputs)

    def test_works_with_non_empty_tuple(self):
        inputs = (1, 2, 3)
        output = OneOf(inputs, items=[(1, 2, 3), 'foo', {'a': 4.0}])
        self.assertEqual(output, inputs)

    def test_error_on_unnamed_iterable_single_item(self):
        log_msg = ['ERROR:root:Value (1, 2, 3) with type tuple is not foo!']
        err_msg = 'Value (1, 2, 3) with type tuple is not foo!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = OneOf((1, 2, 3), items='foo')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_iterable_single_item(self):
        log_msg = ['ERROR:root:Value (1, 2, 3) of '
                   'test with type tuple is not bar!']
        err_msg = 'Value (1, 2, 3) of test with type tuple is not bar!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ItemError) as err:
                _ = OneOf((1, 2, 3), 'test', items='bar')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)


if __name__ == '__main__':
    ut.main()
