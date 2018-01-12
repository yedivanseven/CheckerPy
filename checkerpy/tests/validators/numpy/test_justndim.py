import logging
import unittest as ut
from ....exceptions import IntError, NdimError, CallableError
from ....functional import CompositionOf
try:
    from ....validators.numpy import JustNdim
    from ....types.numpy import _NUMPY_TYPES
    from numpy import array
    from numpy.testing import assert_array_equal
except ImportError:
    no_numpy = True
else:
    no_numpy = False


@ut.skipIf(no_numpy, 'Could not import numpy!')
class TestJustNdim(ut.TestCase):

    def test_error_on_one_ndim_not_convertible_to_int(self):
        err_msg = ('Could not convert given ndim foo '
                   'of type str to required type int!')
        with self.assertRaises(IntError) as err:
            _ = JustNdim(array([1, 2]), ndim='foo')
        self.assertEqual(str(err.exception), err_msg)

    def test_error_on_one_of_two_ndims_not_convertible_to_int(self):
        err_msg = ('Could not convert given ndim bar'
                   ' of type str to required type int!')
        with self.assertRaises(IntError) as err:
            _ = JustNdim(array([1, 2]), ndim=(1, 'bar'))
        self.assertEqual(str(err.exception), err_msg)

    def test_error_on_unnamed_argument_has_no_attribute_ndim(self):
        log_msg = ['ERROR:root:Cannot determine the number '
                   'of dimensions of variable foo with type'
                   ' str because it has no attribute ndim!']
        err_msg = ('Cannot determine the number of dimensions'
                   ' of variable foo with type str because'
                   ' it has no attribute ndim!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(NdimError) as err:
                _ = JustNdim('foo', ndim=2)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_argument_has_no_attribute_ndim(self):
        log_msg = ['ERROR:root:Cannot determine the number '
                   'of dimensions of variable test with type'
                   ' str because it has no attribute ndim!']
        err_msg = ('Cannot determine the number of dimensions'
                   ' of variable test with type str because'
                   ' it has no attribute ndim!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(NdimError) as err:
                _ = JustNdim('foo', 'test', ndim=2)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_sane_array_and_one_ndim(self):
        inputs = array([1, 2, 3])
        output = JustNdim(inputs)
        assert_array_equal(output, inputs)

    def test_error_in_unnamed_array_not_one_ndim(self):
        log_msg = ['ERROR:root:The number of dimensions'
                   ' of array [1 2 3] must be 2, not 1!']
        err_msg = ('The number of dimensions of '
                   'array [1 2 3] must be 2, not 1!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(NdimError) as err:
                _ = JustNdim(array([1, 2, 3]), ndim=2)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_in_named_array_not_one_ndim(self):
        log_msg = ['ERROR:root:The number of dimensions'
                   ' of array test must be 2, not 1!']
        err_msg = ('The number of dimensions of '
                   'array test must be 2, not 1!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(NdimError) as err:
                _ = JustNdim(array([1, 2, 3]), 'test', ndim=2)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_sane_array_and_two_ndims(self):
        inputs = array([1, 2, 3])
        output = JustNdim(inputs, ndim=(1, 2))
        assert_array_equal(output, inputs)

    def test_error_in_unnamed_array_not_one_of_two_ndims(self):
        log_msg = ['ERROR:root:The number of dimensions of '
                   'array [1 2 3] must be one of (2, 3), not 1!']
        err_msg = ('The number of dimensions of array '
                   '[1 2 3] must be one of (2, 3), not 1!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(NdimError) as err:
                _ = JustNdim(array([1, 2, 3]), ndim=(2, 3))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_in_named_array_not_one_of_two_ndims(self):
        log_msg = ['ERROR:root:The number of dimensions of '
                   'array test must be one of (2, 3), not 1!']
        err_msg = ('The number of dimensions of array '
                   'test must be one of (2, 3), not 1!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(NdimError) as err:
                _ = JustNdim(array([1, 2, 3]), 'test', ndim=(2, 3))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_has_numpy_type_checker_attributes(self):
        for numpy_type in _NUMPY_TYPES:
            self.assertTrue(hasattr(JustNdim, numpy_type.__name__))

    def test_numpy_type_checkers_are_type_CompositionOf(self):
        for numpy_type in _NUMPY_TYPES:
            type_checker = getattr(JustNdim, numpy_type.__name__)
            self.assertIsInstance(type_checker, CompositionOf)

    def test_ndim_is_passed_trough_type_checker(self):
        log_msg = ['ERROR:root:The number of dimensions'
                   ' of array [1 2 3] must be 2, not 1!']
        err_msg = ('The number of dimensions of '
                   'array [1 2 3] must be 2, not 1!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(NdimError) as err:
                _ = JustNdim.JustNpNum.JustNdarray(array([1, 2, 3]), ndim=2)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_has_attribute_o(self):
        self.assertTrue(hasattr(JustNdim, 'o'))

    def test_attribute_o_is_callable(self):
        self.assertTrue(callable(JustNdim.o))

    def test_o_returns_composition(self):
        def f(x):
            return x
        composition = JustNdim.o(f)
        self.assertIsInstance(composition, CompositionOf)

    def test_o_raises_error_on_argument_not_callable(self):
        err_msg = ('foo must be a callable that accepts (i) a value,'
                   ' (ii) an optional name for that value, and (iii)'
                   ' any number of keyword arguments!')
        with self.assertRaises(CallableError) as err:
            _ = JustNdim.o('foo')
        self.assertEqual(str(err.exception), err_msg)


if __name__ == '__main__':
    ut.main()
