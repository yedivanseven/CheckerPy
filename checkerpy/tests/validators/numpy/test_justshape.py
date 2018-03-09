import logging
import unittest as ut
from ....functional import CompositionOf
from ....exceptions import IntError, ShapeError, CallableError
try:
    from ....validators.numpy import JustShape
    from ....types.numpy import _NUMPY_TYPES
    from numpy import array
    from numpy.testing import assert_array_equal
except ImportError:
    no_numpy = True
else:
    no_numpy = False


@ut.skipIf(no_numpy, 'Could not import numpy!')
class TestJustShape(ut.TestCase):

    def test_error_on_shape_wrong_type(self):
        err_msg = ('Shape argument must be either a single tuple or a'
                   ' list of tuples of integers, not str like foo!')
        with self.assertRaises(ShapeError) as err:
            _ = JustShape(array([1, 2, 3]), shape='foo')
        self.assertEqual(str(err.exception), err_msg)

    def test_error_on_one_dimension_of_shape_wrong_type(self):
        err_msg = ("Shape argument must be either a single tuple or a list"
                   " of tuples of integers, not tuple like (1, 2, 'bar')!")
        with self.assertRaises(IntError) as err:
            _ = JustShape(array([1, 2, 3]), shape=(1, 2, 'bar'))
        self.assertEqual(str(err.exception), err_msg)

    def test_error_on_one_shape_of_shapes_wrong_type(self):
        err_msg = ("Shape argument must be either a single tuple or a list of"
                   " tuples of integers, not tuple like ((1, 2), 'three')!")
        with self.assertRaises(IntError) as err:
            _ = JustShape(array([1, 2, 3]), shape=((1, 2), 'three'))
        self.assertEqual(str(err.exception), err_msg)

    def test_error_on_one_shape_of_shapes_contains_wrong_type(self):
        err_msg = ("Shape argument must be either a single tuple or a list"
                   " of tuples of integers, not tuple like (3, 'baz')!")
        with self.assertRaises(IntError) as err:
            _ = JustShape(array([1, 2, 3]), shape=((1, 2), (3, 'baz')))
        self.assertEqual(str(err.exception), err_msg)

    def test_error_on_invalid_unnamed_argument(self):
        log_msg = ['ERROR:root:Cannot determine shape of variable foo'
                   ' with type str because it has no attribute shape!']
        err_msg = ('Cannot determine shape of variable foo with '
                   'type str because it has no attribute shape!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ShapeError) as err:
                _ = JustShape('foo')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_invalid_named_argument(self):
        log_msg = ['ERROR:root:Cannot determine shape of variable test'
                   ' with type str because it has no attribute shape!']
        err_msg = ('Cannot determine shape of variable test with '
                   'type str because it has no attribute shape!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ShapeError) as err:
                _ = JustShape('foo', 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_sane_shape_one_tuple(self):
        inputs = array([1, 2, 3])
        output = JustShape(inputs, shape=(3,))
        assert_array_equal(output, inputs)

    def test_works_with_sane_shape_one_list(self):
        inputs = array([1, 2, 3])
        output = JustShape(inputs, shape=[3])
        assert_array_equal(output, inputs)

    def test_works_with_sane_shape_tuple_of_tuples(self):
        inputs = array([1, 2, 3])
        output = JustShape(inputs, shape=((3,), (1, 2)))
        assert_array_equal(output, inputs)

    def test_works_with_sane_shape_list_of_tuples(self):
        inputs = array([1, 2, 3])
        output = JustShape(inputs, shape=[(3,), (1, 2)])
        assert_array_equal(output, inputs)

    def test_works_with_sane_shape_tuple_of_lists(self):
        inputs = array([1, 2, 3])
        output = JustShape(inputs, shape=([3], [1, 2]))
        assert_array_equal(output, inputs)

    def test_works_with_sane_shape_lists_of_lists(self):
        inputs = array([1, 2, 3])
        output = JustShape(inputs, shape=[[3], [1, 2]])
        assert_array_equal(output, inputs)

    def test_works_with_shape_ellipsis(self):
        inputs = array([1, 2, 3])
        output = JustShape(inputs, shape=(...,))
        assert_array_equal(output, inputs)

    def test_works_with_one_shape_of_shapes_containing_ellipsis(self):
        inputs = array([[1, 2, 3], [4, 5, 6]])
        output = JustShape(inputs, shape=[[2], [..., 3]])
        assert_array_equal(output, inputs)

    def test_error_on_unnamed_array_wrong_shape_with_one_shape(self):
        log_msg = ['ERROR:root:Shape of array [1 2 3] must be (2,), not (3,)!']
        err_msg = 'Shape of array [1 2 3] must be (2,), not (3,)!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ShapeError) as err:
                _ = JustShape(array([1, 2, 3]), shape=(2,))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_array_wrong_shape_with_one_shape(self):
        log_msg = ['ERROR:root:Shape of array test must be (2,), not (3,)!']
        err_msg = 'Shape of array test must be (2,), not (3,)!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ShapeError) as err:
                _ = JustShape(array([1, 2, 3]), 'test', shape=(2,))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_unnamed_array_wrong_shape_with_two_shapes(self):
        log_msg = ['ERROR:root:Shape of array [1 2 3] must '
                   'be one of ((2,), (3, 4)), not (3,)!']
        err_msg = ('Shape of array [1 2 3] must be '
                   'one of ((2,), (3, 4)), not (3,)!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ShapeError) as err:
                _ = JustShape(array([1, 2, 3]), shape=((2,), (3, 4)))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_array_wrong_shape_with_two_shapes(self):
        log_msg = ['ERROR:root:Shape of array test must '
                   'be one of ((2,), (3, 4)), not (3,)!']
        err_msg = ('Shape of array test must be one'
                   ' of ((2,), (3, 4)), not (3,)!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ShapeError) as err:
                _ = JustShape(array([1, 2, 3]), 'test', shape=((2,), (3, 4)))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_has_numpy_type_checker_attributes(self):
        for numpy_type in _NUMPY_TYPES:
            self.assertTrue(hasattr(JustShape, numpy_type.__name__))

    def test_numpy_type_checkers_are_type_CompositionOf(self):
        for numpy_type in _NUMPY_TYPES:
            type_checker = getattr(JustShape, numpy_type.__name__)
            self.assertIsInstance(type_checker, CompositionOf)

    def test_shape_is_passed_trough_type_checker(self):
        log_msg = ['ERROR:root:Shape of array [1 2 3] must be (2,), not (3,)!']
        err_msg = 'Shape of array [1 2 3] must be (2,), not (3,)!'
        inputs = array([1, 2, 3])
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ShapeError) as err:
                _ = JustShape.JustNpNum.JustNdarray(inputs, shape=(2,))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_has_attribute_o(self):
        self.assertTrue(hasattr(JustShape, 'o'))

    def test_attribute_o_is_callable(self):
        self.assertTrue(callable(JustShape.o))

    def test_o_returns_composition(self):
        def f(x):
            return x
        composition = JustShape.o(f)
        self.assertIsInstance(composition, CompositionOf)

    def test_o_raises_error_on_argument_not_callable(self):
        err_msg = ('foo must be a callable that accepts (i) a value,'
                   ' (ii) an optional name for that value, and (iii)'
                   ' any number of keyword arguments!')
        with self.assertRaises(CallableError) as err:
            _ = JustShape.o('foo')
        self.assertEqual(str(err.exception), err_msg)


if __name__ == '__main__':
    ut.main()
