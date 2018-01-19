import logging
import unittest as ut
from ...decorators import Bounded
from ...exceptions import LimitError, WrongTypeError, LenError


class TestBoundedInstantiation(ut.TestCase):

    def test_error_on_limit_specification_not_tuple(self):
        err_msg = ('Invalid expression 1 for limits specification'
                   ' of argument at position 0!')
        with self.assertRaises(ValueError) as err:
            @Bounded(1)
            def f(x, y):
                return x + y
        self.assertEqual(str(err.exception), err_msg)

    def test_error_on_limit_specification_tuple_wrong_length(self):
        log_msg = ['ERROR:root:Length of tuple for limits specification of'
                   ' argument at position 0 must be 2, not 3!']
        err_msg = ('Length of tuple for limits specification of'
                   ' argument at position 0 must be 2, not 3!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                @Bounded((1, 2, 3))
                def f(x, y):
                    return x + y
            self.assertEqual(log.output, log_msg)
        self.assertEqual(str(err.exception), err_msg)


class TestBoundedFunctionsArgLimits(ut.TestCase):

    def test_works_with_args_but_no_limits(self):
        @Bounded()
        def f(x, y):
            return x + y
        output = f(1, 2)
        self.assertEqual(output, 3)

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
        log_msg = ['ERROR:root:Value 5 of argument x to function '
                   f'f defined in module {__name__} lies outside '
                   'the allowed interval [1, 3]!']
        err_msg = ('Value 5 of argument x to function f defined in module '
                   f'{__name__} lies outside the allowed interval [1, 3]!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LimitError) as err:
                _ = f(5, 'foo')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_type_error_with_too_few_arg_limits(self):
        @Bounded((1, 3))
        def f(x, y):
            return x + y
        log_msg = ['ERROR:root:Cannot compare type str of argument x to '
                   f'function f defined in module {__name__} with limits'
                   ' of types int and int!']
        err_msg = ('Cannot compare type str of argument x to '
                   f'function f defined in module {__name__} '
                   'with limits of types int and int!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f('foo', 7)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

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
        log_msg = ['ERROR:root:Value 7 of argument y to function '
                   f'f defined in module {__name__} lies outside '
                   'the allowed interval [4, 6]!']
        err_msg = ('Value 7 of argument y to function f defined in module '
                   f'{__name__} lies outside the allowed interval [4, 6]!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LimitError) as err:
                _ = f(2, 7)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_type_error_with_right_number_of_arg_limits(self):
        @Bounded((1, 3), (4, 6))
        def f(x, y):
            return x + y
        log_msg = ['ERROR:root:Cannot compare type str of argument x to '
                   f'function f defined in module {__name__} with limits'
                   ' of types int and int!']
        err_msg = ('Cannot compare type str of argument x to '
                   f'function f defined in module {__name__} '
                   'with limits of types int and int!')
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
        log_msg = ['ERROR:root:Value 7 of argument y to function '
                   f'f defined in module {__name__} lies outside '
                   'the allowed interval [4, 6]!']
        err_msg = ('Value 7 of argument y to function f defined in module '
                   f'{__name__} lies outside the allowed interval [4, 6]!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LimitError) as err:
                _ = f(2, 7)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_type_error_with_too_many_arg_limits(self):
        @Bounded((1, 3), (4, 6), ('a', 'c'))
        def f(x, y):
            return x + y
        log_msg = ['ERROR:root:Cannot compare type str of argument x to '
                   f'function f defined in module {__name__} with limits'
                   ' of types int and int!']
        err_msg = ('Cannot compare type str of argument x to '
                   f'function f defined in module {__name__} '
                   'with limits of types int and int!')
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


class TestBoundedFunctionsArgLimitsOptionalArgsKwargs(ut.TestCase):

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
        log_msg = ['ERROR:root:Cannot compare type str of argument x to '
                   f'function f defined in module {__name__} with limits'
                   ' of types int and int!']
        err_msg = ('Cannot compare type str of argument x to '
                   f'function f defined in module {__name__} '
                   'with limits of types int and int!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f('foo', 5, 1, 3, z=4)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_limit_error_with_optional_args_and_kwargs(self):
        @Bounded((1, 3), (4, 6))
        def f(x, y, *args, **kwargs):
            return x + y + sum(args) + kwargs['z']
        log_msg = ['ERROR:root:Value 6 of argument x to function '
                   f'f defined in module {__name__} lies outside '
                   'the allowed interval [1, 3]!']
        err_msg = ('Value 6 of argument x to function f defined in module '
                   f'{__name__} lies outside the allowed interval [1, 3]!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LimitError) as err:
                _ = f(6, 5, 1, 3, z=4)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_optional_args_are_not_checked(self):
        @Bounded((1, 3), (4, 6), ('a', 'c'))
        def f(x, y, *args):
            return x + y + sum(args)
        output = f(3, 5.0, True, 4.0)
        self.assertEqual(output, 13.0)

    def test_optional_kwargs_are_not_checked(self):
        @Bounded((1, 3), (4, 6), ('a', 'c'))
        def f(x, y, **kwargs):
            return x + y + kwargs['z'] + kwargs['w']
        output = f(3, 5.0, w=1, z=True)
        self.assertEqual(output, 10)

    def test_works_with_required_kwonly_args(self):
        @Bounded((1, 3), (4, 6), ('a', 'c'))
        def f(x, y, *, z):
            return x + y, z
        output = f(1, 5.0, z='b')
        self.assertEqual(output,(6.0, 'b'))

    def test_required_kwonly_args_are_type_checked(self):
        @Bounded((1, 3), (4, 6), ('a', 'c'))
        def f(x, y, *, z='b'):
            return x + y, z
        log_msg = ['ERROR:root:Cannot compare type int of argument z to '
                   f'function f defined in module {__name__} with limits'
                   f' of types str and str!']
        err_msg = ('Cannot compare type int of argument z to '
                   f'function f defined in module {__name__} '
                   f'with limits of types str and str!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f(2, 5.0, z=4)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_required_kwonly_args_are_limit_checked(self):
        @Bounded((1, 3), (4, 6), (7, 9))
        def f(x, y, *, z=8):
            return x + y + z
        log_msg = ['ERROR:root:Value 5 of argument z to function '
                   f'f defined in module {__name__} lies outside '
                   'the allowed interval [7, 9]!']
        err_msg = ('Value 5 of argument z to function f defined in module '
                   f'{__name__} lies outside the allowed interval [7, 9]!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LimitError) as err:
                _ = f(2, 5.0, z=5)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)


class TestBoundedFunctionsKwargLimits(ut.TestCase):

    def test_works_with_too_few_kwarg_limits(self):
        @Bounded(y=(4, 6))
        def f(x, y):
            return x + y
        output = f(2, 5)
        self.assertEqual(output, 7)

    def test_limit_error_with_too_few_kwarg_limits(self):
        @Bounded(y=(1, 3))
        def f(x, y):
            return x + y
        log_msg = ['ERROR:root:Value 5 of argument y to function '
                   f'f defined in module {__name__} lies outside '
                   'the allowed interval [1, 3]!']
        err_msg = ('Value 5 of argument y to function f defined in module '
                   f'{__name__} lies outside the allowed interval [1, 3]!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LimitError) as err:
                _ = f(7, 5)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_type_error_with_too_few_kwarg_limits(self):
        @Bounded(y=(1, 3))
        def f(x, y):
            return x + y
        log_msg = ['ERROR:root:Cannot compare type str of argument y to '
                   f'function f defined in module {__name__} with limits'
                   ' of types int and int!']
        err_msg = ('Cannot compare type str of argument y to '
                   f'function f defined in module {__name__} '
                   'with limits of types int and int!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f(7, 'foo')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_right_number_of_kwarg_limits(self):
        @Bounded(y=(4, 6), x=(1, 3))
        def f(x, y):
            return x + y
        output = f(2, 5)
        self.assertEqual(output, 7)

    def test_limit_error_with_right_number_of_kwarg_limits(self):
        @Bounded(y=(4, 6), x=(1, 3))
        def f(x, y):
            return x + y
        log_msg = ['ERROR:root:Value 7 of argument y to function '
                   f'f defined in module {__name__} lies outside '
                   'the allowed interval [4, 6]!']
        err_msg = ('Value 7 of argument y to function f defined in module '
                   f'{__name__} lies outside the allowed interval [4, 6]!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LimitError) as err:
                _ = f(2, 7)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_type_error_with_right_number_of_kwarg_limits(self):
        @Bounded(y=(4, 6), x=(1, 3))
        def f(x, y):
            return x + y
        log_msg = ['ERROR:root:Cannot compare type str of argument x to '
                   f'function f defined in module {__name__} with limits'
                   ' of types int and int!']
        err_msg = ('Cannot compare type str of argument x to '
                   f'function f defined in module {__name__} '
                   'with limits of types int and int!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f('foo', 7)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_too_many_kwarg_limits(self):
        @Bounded(y=(4, 6), x=(1, 3), z=('a', 'c'))
        def f(x, y):
            return x + y
        output = f(2, 5)
        self.assertEqual(output, 7)

    def test_limit_error_with_too_many_kwarg_limits(self):
        @Bounded(y=(4, 6), x=(1, 3), z=('a', 'c'))
        def f(x, y):
            return x + y
        log_msg = ['ERROR:root:Value 7 of argument y to function '
                   f'f defined in module {__name__} lies outside '
                   'the allowed interval [4, 6]!']
        err_msg = ('Value 7 of argument y to function f defined in module '
                   f'{__name__} lies outside the allowed interval [4, 6]!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LimitError) as err:
                _ = f(2, 7)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_type_error_with_too_many_kwarg_limits(self):
        @Bounded(y=(4, 6), x=(1, 3), z=('a', 'c'))
        def f(x, y):
            return x + y
        log_msg = ['ERROR:root:Cannot compare type str of argument x to '
                   f'function f defined in module {__name__} with limits'
                   ' of types int and int!']
        err_msg = ('Cannot compare type str of argument x to '
                   f'function f defined in module {__name__} '
                   'with limits of types int and int!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f('foo', 7)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_kwarg_limits_but_no_args(self):
        @Bounded(y=(4, 6), x=(1, 3), z=('a', 'c'))
        def f():
            return 7
        output = f()
        self.assertEqual(output, 7)


class TestBoundedFunctionsKwargLimitsOptionalArgsKwargs(ut.TestCase):

    def test_works_with_optional_args_and_kwargs(self):
        @Bounded(y=(4, 6), x=(1, 3))
        def f(x, y, *args, **kwargs):
            return x + y + sum(args) + kwargs['z']
        output = f(2, 5, 1, 3, z=4)
        self.assertEqual(output, 15.0)

    def test_type_error_with_optional_args_and_kwargs(self):
        @Bounded(y=(4, 6), x=(1, 3))
        def f(x, y, *args, **kwargs):
            return x + y + sum(args) + kwargs['z']
        log_msg = ['ERROR:root:Cannot compare type str of argument x to '
                   f'function f defined in module {__name__} with limits'
                   ' of types int and int!']
        err_msg = ('Cannot compare type str of argument x to '
                   f'function f defined in module {__name__} '
                   'with limits of types int and int!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f('foo', 5, 1, 3, z=4)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_limit_error_with_optional_args_and_kwargs(self):
        @Bounded(y=(4, 6), x=(1, 3))
        def f(x, y, *args, **kwargs):
            return x + y + sum(args) + kwargs['z']
        log_msg = ['ERROR:root:Value 6 of argument x to function '
                   f'f defined in module {__name__} lies outside '
                   'the allowed interval [1, 3]!']
        err_msg = ('Value 6 of argument x to function f defined in module '
                   f'{__name__} lies outside the allowed interval [1, 3]!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LimitError) as err:
                _ = f(6, 5, 1, 3, z=4)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_optional_args_are_not_checked(self):
        @Bounded(y=(4, 6), x=(1, 3), z=('a', 'c'))
        def f(x, y, *args):
            return x + y + sum(args)
        output = f(3, 5.0, True, 4.0)
        self.assertEqual(output, 13.0)

    def test_optional_kwargs_are_not_checked(self):
        @Bounded(y=(4, 6), x=(1, 3), z=('a', 'c'))
        def f(x, y, **kwargs):
            return x + y + kwargs['u'] + kwargs['w']
        output = f(3, 5.0, u=1, w=True)
        self.assertEqual(output, 10)

    def test_works_with_required_kwonly_args(self):
        @Bounded(y=(4, 6), x=(1, 3), z=('a', 'c'))
        def f(x, y, *, z):
            return x + y, z
        output = f(1, 5.0, z='b')
        self.assertEqual(output, (6.0, 'b'))

    def test_optional_kwargs_are_type_checked_if_kwarg_limit_specified(self):
        @Bounded(y=(4, 6), x=(1, 3), z=('a', 'c'))
        def f(x, y, *args, **kwargs):
            return x + y + sum(args), kwargs['z']
        log_msg = ['ERROR:root:Cannot compare type int of argument z to '
                   f'function f defined in module {__name__} with limits'
                   f' of types str and str!']
        err_msg = ('Cannot compare type int of argument z to '
                   f'function f defined in module {__name__} '
                   f'with limits of types str and str!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f(2, 5.0, z=4)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_optional_kwargs_are_limit_checked_if_kwarg_limit_specified(self):
        @Bounded(y=(4, 6), x=(1, 3), z=(7, 9))
        def f(x, y, *args, **kwargs):
            return x + y + sum(args) + kwargs['z']
        log_msg = ['ERROR:root:Value 5 of argument z to function '
                   f'f defined in module {__name__} lies outside '
                   'the allowed interval [7, 9]!']
        err_msg = ('Value 5 of argument z to function f defined in module '
                   f'{__name__} lies outside the allowed interval [7, 9]!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LimitError) as err:
                _ = f(2, 5.0, z=5)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)


class TestBoundedFunctionsMixedLimits(ut.TestCase):

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
        log_msg = ['ERROR:root:Value 7 of argument y to function '
                   f'f defined in module {__name__} lies outside '
                   'the allowed interval [4, 6]!']
        err_msg = ('Value 7 of argument y to function f defined in module '
                   f'{__name__} lies outside the allowed interval [4, 6]!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LimitError) as err:
                _ = f(2, 7)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_type_error_with_right_number_of_mixed_limits(self):
        @Bounded((1, 3), y=(4, 6))
        def f(x, y):
            return x + y
        log_msg = ['ERROR:root:Cannot compare type str of argument x to '
                   f'function f defined in module {__name__} with limits'
                   ' of types int and int!']
        err_msg = ('Cannot compare type str of argument x to '
                   f'function f defined in module {__name__} '
                   'with limits of types int and int!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f('foo', 7)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_kwarg_limits_take_precedence_over_arg_limits(self):
        @Bounded((1, 3), ('aaa', 'zzz'), z=('a', 'c'), y=(4, 6))
        def f(x, y):
            return x + y
        log_msg = ['ERROR:root:Cannot compare type str of argument y to '
                   f'function f defined in module {__name__} with limits'
                   ' of types int and int!']
        err_msg = ('Cannot compare type str of argument y to '
                   f'function f defined in module {__name__} '
                   'with limits of types int and int!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f(2, 'foo')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)


class TestBoundedFunctionEllipsis(ut.TestCase):

    def test_works_with_arg_limit_and_ellipsis(self):
        @Bounded((1, 3), ..., (4, 6))
        def f(x, y, z):
            return x + y + z
        output = f(2, 0, 5)
        self.assertEqual(output, 7)

    def test_type_error_with_arg_limit_and_ellipsis(self):
        @Bounded(..., (4, 6))
        def f(x, y):
            return x + y
        log_msg = ['ERROR:root:Value 7 of argument y to function '
                   f'f defined in module {__name__} lies outside '
                   'the allowed interval [4, 6]!']
        err_msg = ('Value 7 of argument y to function f defined in module '
                   f'{__name__} lies outside the allowed interval [4, 6]!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LimitError) as err:
                _ = f(2, 7)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_mixed_limits_and_ellipsis(self):
        @Bounded(..., (1, 6), z=(-1, 1))
        def f(x, y, z):
            return x + y + z
        output = f(2, 5, 0)
        self.assertEqual(output, 7)

    def test_limit_error_with_mixed_limits_and_ellipsis(self):
        @Bounded((1, 3), ..., z=(4, 6))
        def f(x, y, z):
            return x + y + z
        log_msg = ['ERROR:root:Cannot compare type str of argument x to '
                   f'function f defined in module {__name__} with limits'
                   ' of types int and int!']
        err_msg = ('Cannot compare type str of argument x to '
                   f'function f defined in module {__name__} '
                   'with limits of types int and int!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f('foo', 'bar', 5.0)
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
        log_msg = ['ERROR:root:Value 7 of argument y to method m'
                   f' defined in module {__name__} lies outside '
                   'the allowed interval [4, 6]!']
        err_msg = ('Value 7 of argument y to method m defined in module '
                   f'{__name__} lies outside the allowed interval [4, 6]!')
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
        log_msg = ['ERROR:root:Cannot compare type str of argument y to'
                   f' method m defined in module {__name__} with limits'
                   ' of types int and int!']
        err_msg = ('Cannot compare type str of argument y to'
                   f' method m defined in module {__name__} '
                   'with limits of types int and int!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = t.m(2, 'foo')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)


class TestBoundedFunctionsDefaults(ut.TestCase):

    def test_works_with_defaults(self):
        @Bounded((1, 3), z=(4, 6))
        def f(x, y, z=5):
            return x + y + z
        output = f(2, 5)
        self.assertEqual(output, 12)
        output = f(2, 5, 4)
        self.assertEqual(output, 11)
        output = f(2, 5, z=6)
        self.assertEqual(output, 13)

    def test_defaults_are_not_checked(self):
        @Bounded((1, 3), (4, 6), z=('a', 'c'))
        def f(x, y, z=3):
            return x + y + z
        output = f(2, 5)
        self.assertEqual(output, 10)

    def test_limit_error_on_overriding_defaults_with_arg(self):
        @Bounded(z=(1, 3), y=(4, 6))
        def f(x, y, z=2):
            return x + y + z
        log_msg = ['ERROR:root:Value 4 of argument z to function '
                   f'f defined in module {__name__} lies outside '
                   'the allowed interval [1, 3]!']
        err_msg = ('Value 4 of argument z to function f defined in module '
                   f'{__name__} lies outside the allowed interval [1, 3]!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LimitError) as err:
                _ = f(2, 5, 4)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_type_error_on_overriding_defaults_with_kwarg(self):
        @Bounded(z=(1, 3), y=(4, 6))
        def f(x, y, z):
            return x + y + z
        log_msg = ['ERROR:root:Cannot compare type str of argument z to '
                   f'function f defined in module {__name__} with limits'
                   ' of types int and int!']
        err_msg = ('Cannot compare type str of argument z to '
                   f'function f defined in module {__name__} '
                   'with limits of types int and int!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f(2, 5, 'foo')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)


class TestBoundedFunctionTuple(ut.TestCase):

    def test_works_with_tuple(self):
        @Bounded((..., (4, 6)))
        def f(x):
            return x
        inputs = (4, 5)
        output = f(inputs)
        self.assertTupleEqual(output, inputs)

    def test_works_with_empty_tuple(self):
        @Bounded((..., (4, 6)))
        def f(x):
            return x
        inputs = ()
        output = f(inputs)
        self.assertTupleEqual(output, inputs)

    def test_error_on_limit_specs_not_a_tuple(self):
        log_msg = ['ERROR:root:Type of for limits specification of argument'
                   ' at position 0 must be tuple, not list like [4]!']
        err_msg = ('Type of for limits specification of argument '
                   'at position 0 must be tuple, not list like [4]!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                @Bounded((..., [4]))
                def f(x):
                    return x
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_limit_specs_wrong_length(self):
        log_msg = ['ERROR:root:Length of tuple for limits specification'
                   ' of argument at position 0 must be 2, not 3!']
        err_msg = ('Length of tuple for limits specification of'
                   ' argument at position 0 must be 2, not 3!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                @Bounded(((1, 2, 3), ...))
                def f(x):
                    return x
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_argument_not_a_tuple(self):
        @Bounded(((..., 6), ...))
        def f(x):
            return x
        log_msg = ['ERROR:root:Type of argument x to function f defined in '
                   f'module {__name__} must be tuple, not list like [1, 5]!']
        err_msg = ('Type of argument x to function f defined in '
                   f'module {__name__} must be tuple, not list like [1, 5]!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f([1, 5])
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_limit_error_on_tuple_element(self):
        @Bounded((..., (4, 6)))
        def f(x):
            return x
        log_msg = ['ERROR:root:Value 2 of tuple argument x to function f '
                   f'defined in module {__name__} at index 1 lies outside'
                   ' the allowed interval [4, 6]!']
        err_msg = ('Value 2 of tuple argument x to function f defined in '
                   f'module {__name__} at index 1 lies outside the allowed'
                   ' interval [4, 6]!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LimitError) as err:
                _ = f((5, 2))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_type_error_on_tuple_element(self):
        @Bounded(((1, 3), ...))
        def f(x):
            return x
        log_msg = ['ERROR:root:Cannot compare type str of tuple argument x '
                   f'to function f defined in module {__name__} at index 1 '
                   'with limits of types int and int!']
        err_msg = ('Cannot compare type str of tuple argument x to function'
                   f' f defined in module {__name__} at index 1 with limits'
                   ' of types int and int!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f((1, 'a', 2))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)


class TestBoundedFunctionLimitedTuple(ut.TestCase):

    def test_works_with_limited_tuple(self):
        @Bounded(((1, 3), (4, 6)))
        def f(x):
            return x
        inputs = (1, 5)
        output = f(inputs)
        self.assertTupleEqual(output, inputs)

    def test_error_on_not_a_limited_tuple(self):
        @Bounded(((1, 3), (..., 6)))
        def f(x):
            return x
        log_msg = ['ERROR:root:Type of argument x to function f defined in '
                   f'module {__name__} must be tuple, not list like [1, 5]!']
        err_msg = ('Type of argument x to function f defined in '
                   f'module {__name__} must be tuple, not list like [1, 5]!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f([1, 5])
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_limited_tuple_wrong_length(self):
        @Bounded(((1, 3), (4, ...)))
        def f(x):
            return x
        log_msg = ['ERROR:root:Length of tuple argument x to function '
                   f'f defined in module {__name__} must be 2, not 3!']
        err_msg = ('Length of tuple argument x to function f defined'
                   f' in module {__name__} must be 2, not 3!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = f((2, 5, 8))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_limit_error_on_limited_tuple_element(self):
        @Bounded(((..., ...), (4, 6)))
        def f(x):
            return x
        log_msg = ['ERROR:root:Value 2 of element 1 in tuple argument x to'
                   f' function f defined in module {__name__} lies outside'
                   ' the allowed interval [4, 6]!']
        err_msg = ('Value 2 of element 1 in tuple argument x to function f '
                   f'defined in module {__name__} lies outside the allowed '
                   'interval [4, 6]!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LimitError) as err:
                _ = f((1, 2))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_type_error_on_limited_tuple_element(self):
        @Bounded(((1, 3), (4, 6)))
        def f(x):
            return x
        log_msg = ['ERROR:root:Cannot compare type str of element 1 in tuple'
                   f' argument x to function f defined in module {__name__} '
                   'with limits of types int and int!']
        err_msg = ('Cannot compare type str of element 1 in tuple argument x'
                   f' to function f defined in module {__name__} with limits'
                   ' of types int and int!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f((1, 'a'))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)


class TestBoundedFunctionList(ut.TestCase):

    def test_works_with_List(self):
        @Bounded([(1, 3)])
        def f(x):
            return x
        inputs = [1, 2]
        output = f(inputs)
        self.assertListEqual(output, inputs)

    def test_error_on_limit_specs_not_a_tuple(self):
        log_msg = ['ERROR:root:Type of for limits specification of argument'
                   ' at position 0 must be tuple, not int like 4!']
        err_msg = ('Type of for limits specification of argument '
                   'at position 0 must be tuple, not int like 4!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                @Bounded([4])
                def f(x):
                    return x
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_limit_specs_wrong_length(self):
        log_msg = ['ERROR:root:Length of tuple for limits specification'
                   ' of argument at position 0 must be 2, not 3!']
        err_msg = ('Length of tuple for limits specification of'
                   ' argument at position 0 must be 2, not 3!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                @Bounded([(1, 2, 3)])
                def f(x):
                    return x
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_more_than_one_limit_specs(self):
        log_msg = ['ERROR:root:Length of list for limits specification '
                   'of argument at position 0 must be 1, not 2!']
        err_msg = ('Length of list for limits specification'
                   ' of argument at position 0 must be 1, not 2!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                @Bounded([(1, 2), 3])
                def f(x):
                    return x
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_empty_list(self):
        @Bounded([(1, 3)])
        def f(x):
            return x
        inputs = []
        output = f(inputs)
        self.assertListEqual(output, inputs)

    def test_error_on_not_a_list(self):
        @Bounded([(1, 3)])
        def f(x):
            return x
        log_msg = ['ERROR:root:Type of argument x to function f defined in '
                   f'module {__name__} must be list, not tuple like (1, 5)!']
        err_msg = ('Type of argument x to function f defined in '
                   f'module {__name__} must be list, not tuple like (1, 5)!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f((1, 5))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_limit_error_on_list_element(self):
        @Bounded([(1, 3)])
        def f(x):
            return x
        log_msg = ['ERROR:root:Value 5 of list argument x to function f '
                   f'defined in module {__name__} at index 1 lies outside'
                   ' the allowed interval [1, 3]!']
        err_msg = ('Value 5 of list argument x to function f defined in '
                   f'module {__name__} at index 1 lies outside the allowed'
                   ' interval [1, 3]!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LimitError) as err:
                _ = f([2, 5])
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_type_error_on_set_element(self):
        @Bounded([(1, 3)])
        def f(x):
            return x
        log_msg = ['ERROR:root:Cannot compare type str of list argument x '
                   f'to function f defined in module {__name__} at index 1'
                   ' with limits of types int and int!']
        err_msg = ('Cannot compare type str of list argument x to function'
                   f' f defined in module {__name__} at index 1 with limits'
                   ' of types int and int!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f([1, 'a', 2])
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)


class TestBoundedFunctionSet(ut.TestCase):

    def test_works_with_set(self):
        @Bounded({(1, 3)})
        def f(x):
            return x
        inputs = {1, 2}
        output = f(inputs)
        self.assertSetEqual(output, inputs)

    def test_error_on_limit_specs_not_a_tuple(self):
        log_msg = ['ERROR:root:Type of for limits specification of argument'
                   ' at position 0 must be tuple, not int like 4!']
        err_msg = ('Type of for limits specification of argument '
                   'at position 0 must be tuple, not int like 4!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                @Bounded({4})
                def f(x):
                    return x
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_limit_specs_wrong_length(self):
        log_msg = ['ERROR:root:Length of tuple for limits specification'
                   ' of argument at position 0 must be 2, not 3!']
        err_msg = ('Length of tuple for limits specification of'
                   ' argument at position 0 must be 2, not 3!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                @Bounded({(1, 2, 3)})
                def f(x):
                    return x
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_more_than_one_limit_specs(self):
        log_msg = ['ERROR:root:Length of set for limits specification '
                   'of argument at position 0 must be 1, not 2!']
        err_msg = ('Length of set for limits specification'
                   ' of argument at position 0 must be 1, not 2!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                @Bounded({(1, 2), 3})
                def f(x):
                    return x
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_empty_set(self):
        @Bounded({(1, 3)})
        def f(x):
            return x
        inputs = set()
        output = f(inputs)
        self.assertSetEqual(output, inputs)

    def test_error_on_not_a_set(self):
        @Bounded({(1, 3)})
        def f(x):
            return x
        log_msg = ['ERROR:root:Type of argument x to function f defined in '
                   f'module {__name__} must be set, not list like [1, 5]!']
        err_msg = ('Type of argument x to function f defined in '
                   f'module {__name__} must be set, not list like [1, 5]!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f([1, 5])
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_limit_error_on_set_element(self):
        @Bounded({(1, 3)})
        def f(x):
            return x
        log_msg = ['ERROR:root:Value 5 of set argument x to function f '
                   f'defined in module {__name__} lies outside'
                   ' the allowed interval [1, 3]!']
        err_msg = ('Value 5 of set argument x to function f defined in '
                   f'module {__name__} lies outside the allowed'
                   ' interval [1, 3]!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LimitError) as err:
                _ = f({2, 5})
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_type_error_on_set_element(self):
        @Bounded({(1, 3)})
        def f(x):
            return x
        log_msg = ['ERROR:root:Cannot compare type str of set argument x '
                   f'to function f defined in module {__name__} '
                   'with limits of types int and int!']
        err_msg = ('Cannot compare type str of set argument x to function'
                   f' f defined in module {__name__} with limits'
                   ' of types int and int!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f({1, 'a', 2})
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)


if __name__ == '__main__':
    ut.main()
