import logging
import unittest as ut
from ...decorators import Bounded
from ...exceptions import LimitError, WrongTypeError


class TestBoundedInstantiation(ut.TestCase):

    def test_works_with_sane_arg_limits(self):
        @Bounded((1, 3))
        def f(x):
            return x
        output = f(2)
        self.assertEqual(output, 2)

    def test_error_on_arg_limits_not_tuple(self):
        err_msg = ('Type of limits on argument 1 must '
                   'be tuple, not list like [1, 2]!')
        with self.assertRaises(TypeError) as err:
            @Bounded([1, 2])
            def f(x):
                return x
        self.assertEqual(str(err.exception), err_msg)

    def test_error_on_length_of_arg_limit_tuple_not_2(self):
        err_msg = ('There must be exactly 2 limits (lo'
                   ' and hi) for argument 1, not 3!')
        with self.assertRaises(ValueError) as err:
            @Bounded((1, 2, 3))
            def f(x):
                return x
        self.assertEqual(str(err.exception), err_msg)

    def test_works_with_sane_kwarg_limits(self):
        @Bounded(x=(1, 3))
        def f(x):
            return x
        output = f(2)
        self.assertEqual(output, 2)

    def test_error_on_kwarg_limits_not_tuple(self):
        err_msg = ('Type of limits on argument x must '
                   'be tuple, not list like [1, 2]!')
        with self.assertRaises(TypeError) as err:
            @Bounded(x=[1, 2])
            def f(x):
                return x
        self.assertEqual(str(err.exception), err_msg)

    def test_error_on_length_of_kwarg_limit_tuple_not_2(self):
        err_msg = ('There must be exactly 2 limits (lo'
                   ' and hi) for argument x, not 3!')
        with self.assertRaises(ValueError) as err:
            @Bounded(x=(1, 2, 3))
            def f(x):
                return x
        self.assertEqual(str(err.exception), err_msg)


class TestBoundedArgLimits(ut.TestCase):

    def test_works_with_right_number_of_arg_limits(self):
        @Bounded((1, 3), (4, 6))
        def f(x, y):
            return x + y
        output = f(2, 5)
        self.assertEqual(output, 7)

    def test_limit_error_with_right_number_of_arg_limits(self):
        @Bounded((1, 3), (4, 6))
        def f(x, y):
            return x + y
        log_msg = ['ERROR:root:Value 7 of y lies '
                   'outside the allowed interval [4, 6]!',
                   'ERROR:root:An argument of function f defined'
                   f' in module {__name__} is out of bounds!']
        err_msg = ('An argument of function f defined in'
                   f' module {__name__} is out of bounds!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LimitError) as err:
                _ = f(2, 7)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_type_error_with_right_number_of_arg_limits(self):
        @Bounded((1, 3), (4, 6))
        def f(x, y):
            return x + y
        log_msg = ['ERROR:root:Cannot compare type str of'
                   ' x with limits of types int and int!',
                   'ERROR:root:An argument of function f '
                   f'defined in module {__name__} cannot be '
                   f'compared with the corresponding limits!']
        err_msg = (f'An argument of function f defined in module {__name__}'
                   ' cannot be compared with the corresponding limits!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f('foo', 7)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_too_many_arg_limits(self):
        @Bounded((1, 3), (4, 6), ('a', 'c'))
        def f(x, y):
            return x + y
        output = f(2, 5)
        self.assertEqual(output, 7)

    def test_limit_error_with_too_many_arg_limits(self):
        @Bounded((1, 3), (4, 6), ('a', 'c'))
        def f(x, y):
            return x + y
        log_msg = ['ERROR:root:Value 7 of y lies '
                   'outside the allowed interval [4, 6]!',
                   'ERROR:root:An argument of function f defined'
                   f' in module {__name__} is out of bounds!']
        err_msg = ('An argument of function f defined in'
                   f' module {__name__} is out of bounds!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LimitError) as err:
                _ = f(2, 7)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_type_error_with_too_many_arg_limits(self):
        @Bounded((1, 3), (4, 6), ('a', 'c'))
        def f(x, y):
            return x + y
        log_msg = ['ERROR:root:Cannot compare type str of'
                   ' x with limits of types int and int!',
                   'ERROR:root:An argument of function f '
                   f'defined in module {__name__} cannot be '
                   f'compared with the corresponding limits!']
        err_msg = (f'An argument of function f defined in module {__name__}'
                   ' cannot be compared with the corresponding limits!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f('foo', 7)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_arg_limits_but_no_args(self):
        @Bounded((1, 3), (4, 6), ('a', 'c'))
        def f():
            return 7
        output = f()
        self.assertEqual(output, 7)

    def test_works_with_too_few_arg_limits(self):
        @Bounded((1, 3))
        def f(x, y):
            return x + y
        output = f(2, 5)
        self.assertEqual(output, 7)

    def test_limit_error_with_too_few_arg_limits(self):
        @Bounded((1, 3))
        def f(x, y):
            return x + y
        log_msg = ['ERROR:root:Value 5 of x lies '
                   'outside the allowed interval [1, 3]!',
                   'ERROR:root:An argument of function f defined'
                   f' in module {__name__} is out of bounds!']
        err_msg = ('An argument of function f defined in'
                   f' module {__name__} is out of bounds!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LimitError) as err:
                _ = f(5, 'foo')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_type_error_with_too_few_arg_limits(self):
        @Bounded((1, 3))
        def f(x, y):
            return x + y
        log_msg = ['ERROR:root:Cannot compare type str of'
                   ' x with limits of types int and int!',
                   'ERROR:root:An argument of function f '
                   f'defined in module {__name__} cannot be '
                   f'compared with the corresponding limits!']
        err_msg = (f'An argument of function f defined in module {__name__}'
                   ' cannot be compared with the corresponding limits!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f('foo', 7)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_args_but_no_limits(self):
        @Bounded()
        def f(x, y):
            return x + y
        output = f(1, 2)
        self.assertEqual(output, 3)

    def test_works_with_optional_args_and_kwargs(self):
        @Bounded((1, 3), (4, 6))
        def f(x, y, *args, **kwargs):
            return x + y + sum(args) + kwargs['z']
        output = f(2, 5, 1, 3, z=4)
        self.assertEqual(output, 15.0)

    def test_type_error_with_optional_args_and_kwargs(self):
        @Bounded((1, 3), (4, 6))
        def f(x, y, *args, **kwargs):
            return x + y + sum(args) + kwargs['z']
        log_msg = ['ERROR:root:Cannot compare type str of'
                   ' x with limits of types int and int!',
                   'ERROR:root:An argument of function f '
                   f'defined in module {__name__} cannot be '
                   f'compared with the corresponding limits!']
        err_msg = (f'An argument of function f defined in module {__name__}'
                   ' cannot be compared with the corresponding limits!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f('foo', 5, 1, 3, z=4)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_limit_error_with_optional_args_and_kwargs(self):
        @Bounded((1, 3), (4, 6))
        def f(x, y, *args, **kwargs):
            return x + y + sum(args) + kwargs['z']
        log_msg = ['ERROR:root:Value 6 of x lies '
                   'outside the allowed interval [1, 3]!',
                   'ERROR:root:An argument of function f defined'
                   f' in module {__name__} is out of bounds!']
        err_msg = ('An argument of function f defined in'
                   f' module {__name__} is out of bounds!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LimitError) as err:
                _ = f(6, 5, 1, 3, z=4)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)


class TestBoundedKwargLimits(ut.TestCase):

    def test_works_with_right_number_of_kwarg_limits(self):
        @Bounded(y=(1, 3), x=(4, 6))
        def f(x, y):
            return x + y
        output = f(5, 2)
        self.assertEqual(output, 7)

    def test_limit_error_with_right_number_of_kwarg_limits(self):
        @Bounded(y=(1, 3), x=(4, 6))
        def f(x, y):
            return x + y
        log_msg = ['ERROR:root:Value 7 of x lies '
                   'outside the allowed interval [4, 6]!',
                   'ERROR:root:An argument of function f defined'
                   f' in module {__name__} is out of bounds!']
        err_msg = ('An argument of function f defined in'
                   f' module {__name__} is out of bounds!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LimitError) as err:
                _ = f(7, 2)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_type_error_with_right_number_of_kwarg_limits(self):
        @Bounded(y=(1, 3), x=(4, 6))
        def f(x, y):
            return x + y
        log_msg = ['ERROR:root:Cannot compare type str of'
                   ' x with limits of types int and int!',
                   'ERROR:root:An argument of function f '
                   f'defined in module {__name__} cannot be '
                   f'compared with the corresponding limits!']
        err_msg = (f'An argument of function f defined in module {__name__}'
                   ' cannot be compared with the corresponding limits!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f('foo', 2)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_too_many_kwarg_limits(self):
        @Bounded(y=(1, 3), z=('a', 'c'), x=(4, 6))
        def f(x, y):
            return x + y
        output = f(5, 2)
        self.assertEqual(output, 7)

    def test_limit_error_with_too_many_kwarg_limits(self):
        @Bounded(y=(1, 3), z=('a', 'c'), x=(4, 6))
        def f(x, y):
            return x + y
        log_msg = ['ERROR:root:Value 7 of x lies '
                   'outside the allowed interval [4, 6]!',
                   'ERROR:root:An argument of function f defined'
                   f' in module {__name__} is out of bounds!']
        err_msg = ('An argument of function f defined in'
                   f' module {__name__} is out of bounds!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LimitError) as err:
                _ = f(7, 2)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_type_error_with_too_many_kwarg_limits(self):
        @Bounded(y=(1, 3), z=('a', 'c'), x=(4, 6))
        def f(x, y):
            return x + y
        log_msg = ['ERROR:root:Cannot compare type str of'
                   ' x with limits of types int and int!',
                   'ERROR:root:An argument of function f '
                   f'defined in module {__name__} cannot be '
                   f'compared with the corresponding limits!']
        err_msg = (f'An argument of function f defined in module {__name__}'
                   ' cannot be compared with the corresponding limits!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f('foo', 2)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_kwarg_limits_but_no_args(self):
        @Bounded(y=(1, 3), z=('a', 'c'), x=(4, 6))
        def f():
            return 7
        output = f()
        self.assertEqual(output, 7)

    def test_works_with_too_few_kwarg_limits(self):
        @Bounded(y=(1, 3))
        def f(x, y):
            return x + y
        output = f(5, 2)
        self.assertEqual(output, 7)

    def test_limit_error_with_too_few_kwarg_limits(self):
        @Bounded(y=(1, 3))
        def f(x, y):
            return x + y
        log_msg = ['ERROR:root:Value 5 of y lies '
                   'outside the allowed interval [1, 3]!',
                   'ERROR:root:An argument of function f defined'
                   f' in module {__name__} is out of bounds!']
        err_msg = ('An argument of function f defined in'
                   f' module {__name__} is out of bounds!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LimitError) as err:
                _ = f('foo', 5)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_type_error_with_too_few_kwarg_limits(self):
        @Bounded(y=(1, 3))
        def f(x, y):
            return x + y
        log_msg = ['ERROR:root:Cannot compare type str of'
                   ' y with limits of types int and int!',
                   'ERROR:root:An argument of function f '
                   f'defined in module {__name__} cannot be '
                   f'compared with the corresponding limits!']
        err_msg = (f'An argument of function f defined in module {__name__}'
                   ' cannot be compared with the corresponding limits!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f('foo', 'bar')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_kwargs_but_no_limits(self):
        @Bounded()
        def f(x=3, y=2):
            return x + y
        output = f(1)
        self.assertEqual(output, 3)

    def test_works_with_optional_args_and_kwargs(self):
        @Bounded(y=(1, 3), x=(4, 6))
        def f(x, y, *args, **kwargs):
            return x + y + sum(args) + kwargs['z']
        output = f(5, 2, 1, 3, z=4)
        self.assertEqual(output, 15.0)

    def test_type_error_with_optional_args_and_kwargs(self):
        @Bounded(y=(1, 3), x=(4, 6))
        def f(x, y, *args, **kwargs):
            return x + y + sum(args) + kwargs['z']
        log_msg = ['ERROR:root:Cannot compare type str of'
                   ' x with limits of types int and int!',
                   'ERROR:root:An argument of function f '
                   f'defined in module {__name__} cannot be '
                   f'compared with the corresponding limits!']
        err_msg = (f'An argument of function f defined in module {__name__}'
                   ' cannot be compared with the corresponding limits!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f('foo', 5, 1, 3, z=4)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_limit_error_with_optional_args_and_kwargs(self):
        @Bounded(y=(1, 3), x=(4, 6))
        def f(x, y, *args, **kwargs):
            return x + y + sum(args) + kwargs['z']
        log_msg = ['ERROR:root:Value 6 of y lies '
                   'outside the allowed interval [1, 3]!',
                   'ERROR:root:An argument of function f defined'
                   f' in module {__name__} is out of bounds!']
        err_msg = ('An argument of function f defined in'
                   f' module {__name__} is out of bounds!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LimitError) as err:
                _ = f(5, 6, 1, 3, z=4)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)


class TestBoundedMixedLimits(ut.TestCase):

    def test_works_with_right_number_of_mixed_limits(self):
        @Bounded((1, 3), y=(4, 6))
        def f(x, y):
            return x + y
        output = f(2, 5)
        self.assertEqual(output, 7)

    def test_limit_error_with_right_number_of_mixed_limits(self):
        @Bounded((1, 3), y=(4, 6))
        def f(x, y):
            return x + y
        log_msg = ['ERROR:root:Value 7 of y lies '
                   'outside the allowed interval [4, 6]!',
                   'ERROR:root:An argument of function f defined'
                   f' in module {__name__} is out of bounds!']
        err_msg = ('An argument of function f defined in'
                   f' module {__name__} is out of bounds!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LimitError) as err:
                _ = f(2, 7)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_type_error_with_right_number_of_mixed_limits(self):
        @Bounded((1, 3), y=(4, 6))
        def f(x, y):
            return x + y
        log_msg = ['ERROR:root:Cannot compare type str of'
                   ' y with limits of types int and int!',
                   'ERROR:root:An argument of function f '
                   f'defined in module {__name__} cannot be '
                   f'compared with the corresponding limits!']
        err_msg = (f'An argument of function f defined in module {__name__}'
                   ' cannot be compared with the corresponding limits!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f(2, 'foo')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_too_many_mixed_limits(self):
        @Bounded((1, 3), z=('a', 'c'), y=(4, 6))
        def f(x, y):
            return x + y
        output = f(2, 5)
        self.assertEqual(output, 7)

    def test_limit_error_with_too_many_mixed_limits(self):
        @Bounded((1, 3), z=('a', 'c'), y=(4, 6))
        def f(x, y):
            return x + y
        log_msg = ['ERROR:root:Value 7 of y lies '
                   'outside the allowed interval [4, 6]!',
                   'ERROR:root:An argument of function f defined'
                   f' in module {__name__} is out of bounds!']
        err_msg = ('An argument of function f defined in'
                   f' module {__name__} is out of bounds!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LimitError) as err:
                _ = f(2, 7)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_type_error_with_too_many_mixed_limits(self):
        @Bounded((1, 3), z=('a', 'c'), y=(4, 6))
        def f(x, y):
            return x + y
        log_msg = ['ERROR:root:Cannot compare type str of'
                   ' y with limits of types int and int!',
                   'ERROR:root:An argument of function f '
                   f'defined in module {__name__} cannot be '
                   f'compared with the corresponding limits!']
        err_msg = (f'An argument of function f defined in module {__name__}'
                   ' cannot be compared with the corresponding limits!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f(2, 'foo')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_mixed_limits_but_no_args(self):
        @Bounded((1, 3), z=('a', 'c'), y=(4, 6))
        def f():
            return 7
        output = f()
        self.assertEqual(output, 7)

    def test_works_with_too_few_mixed_limits(self):
        @Bounded((1, 3), z=(4, 6))
        def f(x, y, z):
            return x + y + z
        output = f(2, 7, 5)
        self.assertEqual(output, 14)

    def test_limit_error_with_too_few_mixed_limits(self):
        @Bounded((1, 3), z=(4, 6))
        def f(x, y, z):
            return x + y + z
        log_msg = ['ERROR:root:Value 7 of z lies '
                   'outside the allowed interval [4, 6]!',
                   'ERROR:root:An argument of function f defined'
                   f' in module {__name__} is out of bounds!']
        err_msg = ('An argument of function f defined in'
                   f' module {__name__} is out of bounds!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LimitError) as err:
                _ = f(2, 'foo', 7)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_type_error_with_too_few_mixed_limits(self):
        @Bounded((1, 3), z=(4, 6))
        def f(x, y, z):
            return x + y + z
        log_msg = ['ERROR:root:Cannot compare type str of'
                   ' z with limits of types int and int!',
                   'ERROR:root:An argument of function f '
                   f'defined in module {__name__} cannot be '
                   f'compared with the corresponding limits!']
        err_msg = (f'An argument of function f defined in module {__name__}'
                   ' cannot be compared with the corresponding limits!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f(2, 'foo', 'bar')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_optional_args_and_kwargs(self):
        @Bounded((1, 3), z=(4, 6))
        def f(x, y, z, *args, **kwargs):
            return x + y + z + sum(args) + kwargs['u']
        output = f(2, 7, 5, 3, 0, u=4)
        self.assertEqual(output, 21)

    def test_type_error_with_optional_args_and_kwargs(self):
        @Bounded((1, 3), z=(4, 6))
        def f(x, y, z, *args, **kwargs):
            return x + y + z + sum(args) + kwargs['u']
        log_msg = ['ERROR:root:Cannot compare type str of'
                   ' z with limits of types int and int!',
                   'ERROR:root:An argument of function f '
                   f'defined in module {__name__} cannot be '
                   f'compared with the corresponding limits!']
        err_msg = (f'An argument of function f defined in module {__name__}'
                   ' cannot be compared with the corresponding limits!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f(2, 7, 'foo', 3, 0, u=4)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_limit_error_with_optional_args_and_kwargs(self):
        @Bounded((1, 3), z=(4, 6))
        def f(x, y, z, *args, **kwargs):
            return x + y + z + sum(args) + kwargs['u']
        log_msg = ['ERROR:root:Value 7 of z lies '
                   'outside the allowed interval [4, 6]!',
                   'ERROR:root:An argument of function f defined'
                   f' in module {__name__} is out of bounds!']
        err_msg = ('An argument of function f defined in'
                   f' module {__name__} is out of bounds!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LimitError) as err:
                _ = f(2, 9, 7, 3, 0, u=4)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)


class TestBoundedMethod(ut.TestCase):

    def test_works_on_methods(self):
        class Test:
            @Bounded((1, 3), z=('a', 'c'), y=(4, 6))
            def m(self, x, y):
                return x + y
        t = Test()
        output = t.m(2, 5)
        self.assertEqual(output, 7)

    def test_limit_error_on_method(self):
        class Test:
            @Bounded((1, 3), z=('a', 'c'), y=(4, 6))
            def m(self, x, y):
                return x + y
        t = Test()
        log_msg = ['ERROR:root:Value 7 of y lies '
                   'outside the allowed interval [4, 6]!',
                   'ERROR:root:An argument of method m defined'
                   f' in module {__name__} is out of bounds!']
        err_msg = ('An argument of method m defined in'
                   f' module {__name__} is out of bounds!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LimitError) as err:
                _ = t.m(2, 7)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_type_error_on_method(self):
        class Test:
            @Bounded((1, 3), z=('a', 'c'), y=(4, 6))
            def m(self, x, y):
                return x + y
        t = Test()
        log_msg = ['ERROR:root:Cannot compare type str of'
                   ' y with limits of types int and int!',
                   'ERROR:root:An argument of method m '
                   f'defined in module {__name__} cannot be '
                   f'compared with the corresponding limits!']
        err_msg = (f'An argument of method m defined in module {__name__}'
                   ' cannot be compared with the corresponding limits!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = t.m(2, 'foo')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)


if __name__ == '__main__':
    ut.main()
