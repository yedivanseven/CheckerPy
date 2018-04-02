import logging
import unittest as ut
from ....exceptions import IntError, SizeError, CallableError
from ....functional import CompositionOf
try:
    from ....validators.numpy import JustSize
    from ....types.numpy import _NUMPY_TYPES
    from numpy import array
    from numpy.testing import assert_array_equal
except ImportError:
    no_numpy = True
else:
    no_numpy = False


@ut.skipIf(no_numpy, 'Could not import numpy!')
class TestJustNdim(ut.TestCase):

    def test_error_on_one_size_not_convertible_to_int(self):
        err_msg = ('Could not convert given size f '
                   'of type str to required type int!')
        with self.assertRaises(IntError) as err:
            _ = JustSize(array([1, 2]), size='foo')
        self.assertEqual(str(err.exception), err_msg)

    def test_error_on_one_of_two_sizes_not_convertible_to_int(self):
        err_msg = ('Could not convert given size bar'
                   ' of type str to required type int!')
        with self.assertRaises(IntError) as err:
            _ = JustSize(array([1, 2]), size=(1, 'bar'))
        self.assertEqual(str(err.exception), err_msg)

    def test_error_on_unnamed_argument_has_no_attribute_size(self):
        log_msg = ['ERROR:root:Cannot determine the number '
                   'of elements in variable foo with type'
                   ' str because it has no attribute size!']
        err_msg = ('Cannot determine the number of elements'
                   ' in variable foo with type str because'
                   ' it has no attribute size!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(SizeError) as err:
                _ = JustSize('foo', size=2)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_argument_has_no_attribute_size(self):
        log_msg = ['ERROR:root:Cannot determine the number '
                   'of elements in variable test with type'
                   ' str because it has no attribute size!']
        err_msg = ('Cannot determine the number of elements'
                   ' in variable test with type str because'
                   ' it has no attribute size!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(SizeError) as err:
                _ = JustSize('foo', 'test', size=2)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_sane_array_and_one_size(self):
        inputs = array([1, 2, 3])
        output = JustSize(inputs, size=3)
        assert_array_equal(output, inputs)

    def test_error_in_unnamed_array_not_one_size(self):
        log_msg = ['ERROR:root:The number of elements '
                   'in array [1 2 3] must be 2, not 3!']
        err_msg = ('The number of elements in '
                   'array [1 2 3] must be 2, not 3!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(SizeError) as err:
                _ = JustSize(array([1, 2, 3]), size=2)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_in_named_array_not_one_size(self):
        log_msg = ['ERROR:root:The number of elements '
                   'in array test must be 2, not 3!']
        err_msg = ('The number of elements in '
                   'array test must be 2, not 3!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(SizeError) as err:
                _ = JustSize(array([1, 2, 3]), 'test', size=2)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_sane_array_and_two_sizes(self):
        inputs = array([1, 2, 3])
        output = JustSize(inputs, size=(2, 3))
        assert_array_equal(output, inputs)

    def test_error_in_unnamed_array_not_one_of_two_sizes(self):
        log_msg = ['ERROR:root:The number of elements in '
                   'array [1 2 3] must be one of (1, 2), not 3!']
        err_msg = ('The number of elements in array '
                   '[1 2 3] must be one of (1, 2), not 3!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(SizeError) as err:
                _ = JustSize(array([1, 2, 3]), size=(1, 2))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_in_named_array_not_one_of_two_sizes(self):
        log_msg = ['ERROR:root:The number of elements in '
                   'array test must be one of (1, 2), not 3!']
        err_msg = ('The number of elements in array '
                   'test must be one of (1, 2), not 3!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(SizeError) as err:
                _ = JustSize(array([1, 2, 3]), 'test', size=(1, 2))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_has_numpy_type_checker_attributes(self):
        for numpy_type in _NUMPY_TYPES:
            self.assertTrue(hasattr(JustSize, numpy_type.__name__))

    def test_numpy_type_checkers_are_type_CompositionOf(self):
        for numpy_type in _NUMPY_TYPES:
            type_checker = getattr(JustSize, numpy_type.__name__)
            self.assertIsInstance(type_checker, CompositionOf)

    def test_size_is_passed_trough_type_checker(self):
        log_msg = ['ERROR:root:The number of elements '
                   'in array [1 2 3] must be 2, not 3!']
        err_msg = ('The number of elements in '
                   'array [1 2 3] must be 2, not 3!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(SizeError) as err:
                _ = JustSize.JustNpNum.JustNdarray(array([1, 2, 3]), size=2)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_has_attribute_o(self):
        self.assertTrue(hasattr(JustSize, 'o'))

    def test_attribute_o_is_callable(self):
        self.assertTrue(callable(JustSize.o))

    def test_o_returns_composition(self):
        def f(x):
            return x
        composition = JustSize.o(f)
        self.assertIsInstance(composition, CompositionOf)

    def test_o_raises_error_on_argument_not_callable(self):
        err_msg = ('foo must be a callable that accepts (i) a value,'
                   ' (ii) an optional name for that value, and (iii)'
                   ' any number of keyword arguments!')
        with self.assertRaises(CallableError) as err:
            _ = JustSize.o('foo')
        self.assertEqual(str(err.exception), err_msg)


if __name__ == '__main__':
    ut.main()
