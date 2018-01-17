import logging
import unittest as ut
from ...decorators import Typed
from ...exceptions import WrongTypeError, LenError


class TestTypedFunctionsSingleArgType(ut.TestCase):

    def test_works_with_no_types(self):
        @Typed()
        def f(x, y):
            return x + y
        output = f(1, 2.0)
        self.assertEqual(output, 3.0)

    def test_works_with_single_arg_type_too_few_types(self):
        @Typed(int)
        def f(x, y):
            return x + y
        output = f(1, 2.0)
        self.assertEqual(output, 3.0)

    def test_error_with_single_arg_type_too_few_types(self):
        @Typed(int)
        def f(x, y):
            return x + y
        log_msg = ['ERROR:root:Type of x must be int, not str like foo!',
                   'ERROR:root:An argument of function f defined'
                   f' in module {__name__} is of wrong type!']
        err_msg = ('An argument of function f defined in '
                   f'module {__name__} is of wrong type!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f('foo', 2.0)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_single_arg_type_right_number_of_types(self):
        @Typed(int, float)
        def f(x, y):
            return x + y
        output = f(1, 2.0)
        self.assertEqual(output, 3.0)

    def test_error_with_single_arg_type_right_number_of_types(self):
        @Typed(int, float)
        def f(x, y):
            return x + y
        log_msg = ['ERROR:root:Type of y must be float, not str like foo!',
                   'ERROR:root:An argument of function f defined'
                   f' in module {__name__} is of wrong type!']
        err_msg = ('An argument of function f defined in '
                   f'module {__name__} is of wrong type!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f(1, 'foo')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_single_arg_type_too_many_types(self):
        @Typed(int, float, str)
        def f(x, y):
            return x + y
        output = f(1, 2.0)
        self.assertEqual(output, 3.0)

    def test_error_with_single_arg_type_too_many_types(self):
        @Typed(int, float, str)
        def f(x, y):
            return x + y
        log_msg = ['ERROR:root:Type of y must be float, not str like foo!',
                   'ERROR:root:An argument of function f defined'
                   f' in module {__name__} is of wrong type!']
        err_msg = ('An argument of function f defined in '
                   f'module {__name__} is of wrong type!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f(1, 'foo')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_single_arg_type_no_args(self):
        @Typed(int, float, str)
        def f():
            return 3.0
        output = f()
        self.assertEqual(output, 3.0)


class TestTypedFunctionsTwoArgTypes(ut.TestCase):

    def test_works_with_two_arg_types_too_few_types(self):
        @Typed((int, float))
        def f(x, y):
            return x + y
        output = f(1, 2.0)
        self.assertEqual(output, 3.0)

    def test_error_with_two_arg_types_too_few_types(self):
        @Typed((int, float))
        def f(x, y):
            return x + y
        log_msg = ["ERROR:root:Type of x must be one of "
                   "('int', 'float'), not str like foo!",
                   'ERROR:root:An argument of function f defined'
                   f' in module {__name__} is of wrong type!']
        err_msg = ('An argument of function f defined in '
                   f'module {__name__} is of wrong type!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f('foo', 2.0)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_two_arg_types_right_number_of_types(self):
        @Typed((int, float), (float, complex))
        def f(x, y):
            return x + y
        output = f(1, 2.0)
        self.assertEqual(output, 3.0)

    def test_error_with_two_arg_types_right_number_of_types(self):
        @Typed((int, float), (float, complex))
        def f(x, y):
            return x + y
        log_msg = ["ERROR:root:Type of y must be one of "
                   "('float', 'complex'), not str like foo!",
                   'ERROR:root:An argument of function f defined'
                   f' in module {__name__} is of wrong type!']
        err_msg = ('An argument of function f defined in '
                   f'module {__name__} is of wrong type!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f(1, 'foo')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_two_arg_types_too_many_types(self):
        @Typed((int, float), (float, complex), (str, tuple))
        def f(x, y):
            return x + y
        output = f(1, 2.0)
        self.assertEqual(output, 3.0)

    def test_error_with_two_arg_types_too_many_types(self):
        @Typed((int, float), (float, complex), (str, tuple))
        def f(x, y):
            return x + y
        log_msg = ["ERROR:root:Type of y must be one of "
                   "('float', 'complex'), not str like foo!",
                   'ERROR:root:An argument of function f defined'
                   f' in module {__name__} is of wrong type!']
        err_msg = ('An argument of function f defined in '
                   f'module {__name__} is of wrong type!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f(1, 'foo')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_two_arg_types_no_args(self):
        @Typed((int, float), (str, tuple))
        def f():
            return 3.0
        output = f()
        self.assertEqual(output, 3.0)


class TestTypedFunctionsMixedArgTypes(ut.TestCase):

    def test_works_with_mixed_arg_types_too_few_types(self):
        @Typed((int, str), float)
        def f(x, y, z):
            return x + y

        output = f(1, 2.0, 'bar')
        self.assertEqual(output, 3.0)

    def test_error_with_mixed_arg_types_too_few_types(self):
        @Typed((int, str), float)
        def f(x, y, z):
            return x + y

        log_msg = ['ERROR:root:Type of y must be float, not str like foo!',
                   'ERROR:root:An argument of function f defined'
                   f' in module {__name__} is of wrong type!']
        err_msg = ('An argument of function f defined in '
                   f'module {__name__} is of wrong type!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f(1, 'foo', 'bar')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_mixed_arg_types_right_number_of_types(self):
        @Typed((int, str), float)
        def f(x, y):
            return x + y
        output = f(1, 2.0)
        self.assertEqual(output, 3.0)

    def test_error_with_mixed_arg_types_right_number_of_types(self):
        @Typed((int, str), float)
        def f(x, y):
            return x + y
        log_msg = ['ERROR:root:Type of y must be float, not str like foo!',
                   'ERROR:root:An argument of function f defined'
                   f' in module {__name__} is of wrong type!']
        err_msg = ('An argument of function f defined in '
                   f'module {__name__} is of wrong type!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f(1, 'foo')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_mixed_arg_types_too_many_types(self):
        @Typed((int, str), float, (str, tuple))
        def f(x, y):
            return x + y
        output = f(1, 2.0)
        self.assertEqual(output, 3.0)

    def test_error_with_mixed_arg_types_too_many_types(self):
        @Typed((int, str), float, (str, tuple))
        def f(x, y):
            return x + y
        log_msg = ['ERROR:root:Type of y must be float, not str like foo!',
                   'ERROR:root:An argument of function f defined'
                   f' in module {__name__} is of wrong type!']
        err_msg = ('An argument of function f defined in '
                   f'module {__name__} is of wrong type!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f(1, 'foo')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_mixed_arg_types_no_args(self):
        @Typed((int, float), str)
        def f():
            return 3.0
        output = f()
        self.assertEqual(output, 3.0)


class TestTypedFunctionsMixedArgTypesOptionalArgsKwargs(ut.TestCase):

    def test_works_with_optional_args_and_kwargs(self):
        @Typed((int, str), float)
        def f(x, y, *args, **kwargs):
            return x + y + sum(args) + kwargs['z']
        output = f(1, 2.0, 3, 4, w=3, z=5)
        self.assertEqual(output, 15.0)

    def test_error_with_optional_args_and_kwargs(self):
        @Typed((int, str), float)
        def f(x, y, *args, **kwargs):
            return x + y + sum(args) + kwargs['z']
        log_msg = ['ERROR:root:Type of y must be float, not str like foo!',
                   'ERROR:root:An argument of function f defined'
                   f' in module {__name__} is of wrong type!']
        err_msg = ('An argument of function f defined in '
                   f'module {__name__} is of wrong type!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f(1, 'foo', 3, 4, z=5)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_optional_args_are_not_checked(self):
        @Typed((int, bool), float, int)
        def f(x, y, *args):
            return x + y + sum(args)
        output = f(3, 2.0, True, 4.0)
        self.assertEqual(output, 10.0)

    def test_optional_kwargs_are_not_checked(self):
        @Typed((int, bool), float, int)
        def f(x, y, **kwargs):
            return x + y + kwargs['z'] + kwargs['w']
        output = f(3, 2.0, w=1, z=True)
        self.assertEqual(output, 7.0)


class TestTypedFunctionsSingleKwargType(ut.TestCase):

    def test_works_with_single_kwarg_type_too_few_types(self):
        @Typed(y=float)
        def f(x, y):
            return x + y
        output = f(1, 2.0)
        self.assertEqual(output, 3.0)

    def test_error_with_single_kwarg_type_too_few_types(self):
        @Typed(y=float)
        def f(x, y):
            return x + y
        log_msg = ['ERROR:root:Type of y must be float, not str like bar!',
                   'ERROR:root:An argument of function f defined'
                   f' in module {__name__} is of wrong type!']
        err_msg = ('An argument of function f defined in '
                   f'module {__name__} is of wrong type!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f('foo', 'bar')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_single_kwarg_type_right_number_of_types(self):
        @Typed(y=float, x=int)
        def f(x, y):
            return x + y
        output = f(1, 2.0)
        self.assertEqual(output, 3.0)

    def test_error_with_single_kwarg_type_right_number_of_types(self):
        @Typed(y=float, x=int)
        def f(x, y):
            return x + y
        log_msg = ['ERROR:root:Type of y must be float, not str like foo!',
                   'ERROR:root:An argument of function f defined'
                   f' in module {__name__} is of wrong type!']
        err_msg = ('An argument of function f defined in '
                   f'module {__name__} is of wrong type!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f(1, 'foo')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_single_kwarg_type_too_many_types(self):
        @Typed(y=float, x=int, z=str)
        def f(x, y):
            return x + y
        output = f(1, 2.0)
        self.assertEqual(output, 3.0)

    def test_error_with_single_kwarg_type_too_many_types(self):
        @Typed(y=float, x=int, z=str)
        def f(x, y):
            return x + y
        log_msg = ['ERROR:root:Type of y must be float, not str like foo!',
                   'ERROR:root:An argument of function f defined'
                   f' in module {__name__} is of wrong type!']
        err_msg = ('An argument of function f defined in '
                   f'module {__name__} is of wrong type!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f(1, 'foo')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_single_kwarg_type_no_args(self):
        @Typed(y=float, z=str)
        def f():
            return 3.0
        output = f()
        self.assertEqual(output, 3.0)


class TestTypedFunctionsTwoKwargTypes(ut.TestCase):

    def test_works_with_two_arg_types_too_few_types(self):
        @Typed(y=(int, float))
        def f(x, y):
            return x + y
        output = f(1, 2.0)
        self.assertEqual(output, 3.0)

    def test_error_with_two_arg_types_too_few_types(self):
        @Typed(y=(int, float))
        def f(x, y):
            return x + y
        log_msg = ["ERROR:root:Type of y must be one of "
                   "('int', 'float'), not str like bar!",
                   'ERROR:root:An argument of function f defined'
                   f' in module {__name__} is of wrong type!']
        err_msg = ('An argument of function f defined in '
                   f'module {__name__} is of wrong type!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f('foo', 'bar')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_two_kwarg_types_right_number_of_types(self):
        @Typed(y=(int, float), x=(float, complex))
        def f(x, y):
            return x + y
        output = f(1.0, 2)
        self.assertEqual(output, 3.0)

    def test_error_with_two_kwarg_types_right_number_of_types(self):
        @Typed(y=(int, float), x=(float, complex))
        def f(x, y):
            return x + y
        log_msg = ["ERROR:root:Type of y must be one of "
                   "('int', 'float'), not str like foo!",
                   'ERROR:root:An argument of function f defined'
                   f' in module {__name__} is of wrong type!']
        err_msg = ('An argument of function f defined in '
                   f'module {__name__} is of wrong type!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f(1.0, 'foo')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_two_kwarg_types_too_many_types(self):
        @Typed(y=(int, float), x=(float, complex), z=(str, tuple))
        def f(x, y):
            return x + y
        output = f(1.0, 2)
        self.assertEqual(output, 3.0)

    def test_error_with_two_kwarg_types_too_many_types(self):
        @Typed(y=(int, float), x=(float, complex), z=(str, tuple))
        def f(x, y):
            return x + y
        log_msg = ["ERROR:root:Type of y must be one of "
                   "('int', 'float'), not str like foo!",
                   'ERROR:root:An argument of function f defined'
                   f' in module {__name__} is of wrong type!']
        err_msg = ('An argument of function f defined in '
                   f'module {__name__} is of wrong type!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f(1.0, 'foo')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_two_kwarg_types_no_args(self):
        @Typed(y=(int, float), x=(float, complex))
        def f():
            return 3.0
        output = f()
        self.assertEqual(output, 3.0)


class TestTypedFunctionsMixedKwargTypes(ut.TestCase):

    def test_works_with_mixed_kwarg_types_too_few_types(self):
        @Typed(z=(int, str), y=float)
        def f(x, y, z):
            return x + y + z
        output = f(1, 2.0, 3)
        self.assertEqual(output, 6.0)

    def test_error_with_mixed_kwarg_types_too_few_types(self):
        @Typed(z=(int, str), y=float)
        def f(x, y, z):
            return x + y + z
        log_msg = ['ERROR:root:Type of y must be float, not str like foo!',
                   'ERROR:root:An argument of function f defined'
                   f' in module {__name__} is of wrong type!']
        err_msg = ('An argument of function f defined in '
                   f'module {__name__} is of wrong type!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f(1, 'foo', 3)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_mixed_kwarg_types_right_number_of_types(self):
        @Typed(y=(int, str), x=float)
        def f(x, y):
            return x + y
        output = f(1.0, 2)
        self.assertEqual(output, 3.0)

    def test_error_with_mixed_kwarg_types_right_number_of_types(self):
        @Typed(y=(int, str), x=float)
        def f(x, y):
            return x + y
        log_msg = ['ERROR:root:Type of x must be float, not str like foo!',
                   'ERROR:root:An argument of function f defined'
                   f' in module {__name__} is of wrong type!']
        err_msg = ('An argument of function f defined in '
                   f'module {__name__} is of wrong type!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f('foo', 2.0)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_mixed_kwarg_types_too_many_types(self):
        @Typed(y=(int, str), x=float, z=(str, tuple))
        def f(x, y):
            return x + y
        output = f(1.0, 2)
        self.assertEqual(output, 3.0)

    def test_error_with_mixed_kwarg_types_too_many_types(self):
        @Typed(y=(int, str), x=float, z=(str, tuple))
        def f(x, y):
            return x + y
        log_msg = ['ERROR:root:Type of x must be float, not str like foo!',
                   'ERROR:root:An argument of function f defined'
                   f' in module {__name__} is of wrong type!']
        err_msg = ('An argument of function f defined in '
                   f'module {__name__} is of wrong type!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f('foo', 2)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_mixed_kwarg_types_no_args(self):
        @Typed(y=(int, float), z=str)
        def f():
            return 3.0
        output = f()
        self.assertEqual(output, 3.0)


class TestTypedFunctionsMixedKwargTypesOptionalArgsKwargs(ut.TestCase):

    def test_works_with_optional_args_and_kwargs(self):
        @Typed(y=(int, str), x=float)
        def f(x, y, *args, **kwargs):
            return x + y + sum(args) + kwargs['z']
        output = f(1.0, 2, 3, 4, z=5)
        self.assertEqual(output, 15.0)

    def test_error_with_optional_args_and_kwargs(self):
        @Typed(y=(int, str), x=float)
        def f(x, y, *args, **kwargs):
            return x + y + sum(args) + kwargs['z']
        log_msg = ["ERROR:root:Type of y must be one of "
                   "('int', 'str'), not float like 2.0!",
                   'ERROR:root:An argument of function f defined'
                   f' in module {__name__} is of wrong type!']
        err_msg = ('An argument of function f defined in '
                   f'module {__name__} is of wrong type!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f(1.0, 2.0, 3, 4, z=5)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_optional_args_are_not_checked(self):
        @Typed(y=float, x=(int, bool), z=str)
        def f(x, y, *args):
            return x + y + sum(args)
        output = f(3, 2.0, True, 4.0)
        self.assertEqual(output, 10.0)

    def test_optional_kwargs_not_checked(self):
        @Typed(y=float, x=(int, bool), z=str)
        def f(x, y, **kwargs):
            return x + y + kwargs['w']
        output = f(3, 2.0, w=True)
        self.assertEqual(output, 6.0)

    def test_optional_kwargs_are_checked_if_kwarg_type_specified(self):
        @Typed(y=float, x=(int, bool), z=str)
        def f(x, y, **kwargs):
            return x + y + kwargs['w'] + kwargs['z']
        log_msg = ['ERROR:root:Type of z must be str, not bool like False!',
                   'ERROR:root:An argument of function f defined'
                   f' in module {__name__} is of wrong type!']
        err_msg = ('An argument of function f defined in '
                   f'module {__name__} is of wrong type!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f(3, 2.0, w=True, z=False)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)


class TestTypedFunctionsArgAndKwargTypes(ut.TestCase):

    def test_works_with_arg_and_kwarg_types(self):
        @Typed((int, str), v=float, u=int)
        def f(x, y, z, u, v):
            return x + y + z + u + v
        output = f(1, 2.0, 3, 4, 5.0)
        self.assertEqual(output, 15.0)

    def test_error_with_arg_and_kwarg_types(self):
        @Typed((int, float), v=float, u=(int, str))
        def f(x, y, z, u, v):
            return x + y + z + u + v
        log_msg = ["ERROR:root:Type of u must be one of "
                   "('int', 'str'), not float like 4.0!",
                   'ERROR:root:An argument of function f defined'
                   f' in module {__name__} is of wrong type!']
        err_msg = ('An argument of function f defined in '
                   f'module {__name__} is of wrong type!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f(1.0, 'foo', 'bar', 4.0, 5.0)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_kwarg_types_take_precedence_over_arg_types(self):
        @Typed(int, float, bool, z=str)
        def f(x, y, z):
            return x + y + z
        log_msg = ['ERROR:root:Type of z must be str, not bool like True!',
                   'ERROR:root:An argument of function f defined '
                   f'in module {__name__} is of wrong type!']
        err_msg = ('An argument of function f defined in '
                   f'module {__name__} is of wrong type!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f(1, 2.0, True)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)


class TestTypedFunctionsEllipsis(ut.TestCase):

    def test_works_with_arg_type_and_ellipsis(self):
        @Typed(int, ..., float)
        def f(x, y, z):
            return x + y + z
        output = f(1, True, 2.0)
        self.assertEqual(output, 4.0)

    def test_error_with_arg_type_and_ellipsis(self):
        @Typed(int, ..., str)
        def f(x, y, z):
            return x + y + z
        log_msg = ['ERROR:root:Type of z must be str, not bool like True!',
                   'ERROR:root:An argument of function f defined '
                   f'in module {__name__} is of wrong type!']
        err_msg = ('An argument of function f defined in '
                   f'module {__name__} is of wrong type!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f(1, 2.0, True)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_kwarg_types_and_ellipsis(self):
        @Typed(..., bool, z=(float, tuple))
        def f(x, y, z):
            return x + y + z
        output = f(1, True, 2.0)
        self.assertEqual(output, 4.0)

    def test_error_with_kwarg_types_and_ellipsis(self):
        @Typed(int, ..., z=(float, tuple))
        def f(x, y, z):
            return x + y + z
        log_msg = ["ERROR:root:Type of z must be one of "
                   "('float', 'tuple'), not bool like True!",
                   'ERROR:root:An argument of function f defined '
                   f'in module {__name__} is of wrong type!']
        err_msg = ('An argument of function f defined in '
                   f'module {__name__} is of wrong type!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f(1, 2.0, True)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)


class TestTypedFunctionsDefaults(ut.TestCase):

    def test_works_with_defaults(self):
        @Typed((int, float), z=int)
        def f(x, y, z=3):
            return x + y + z
        output = f(1.0, 2)
        self.assertEqual(output, 6)
        output = f(1.0, 2, 4)
        self.assertEqual(output, 7)
        output = f(1.0, 2, z=5)
        self.assertEqual(output, 8)

    def test_error_on_overring_defaults_with_arg(self):
        @Typed(y=(int, float), z=str)
        def f(x, y, z=3):
            return x + y + z
        log_msg = ['ERROR:root:Type of z must be str, not bool like True!',
                   'ERROR:root:An argument of function f defined'
                   f' in module {__name__} is of wrong type!']
        err_msg = ('An argument of function f defined in '
                   f'module {__name__} is of wrong type!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f(1, 2.0, True)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_overring_defaults_with_kwarg(self):
        @Typed(y=(int, float), z=str)
        def f(x, y, z=3):
            return x + y + z
        log_msg = ['ERROR:root:Type of z must be str, not bool like True!',
                   'ERROR:root:An argument of function f defined'
                   f' in module {__name__} is of wrong type!']
        err_msg = ('An argument of function f defined in '
                   f'module {__name__} is of wrong type!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f(1, 2.0, z=True)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_defaults_are_not_checked(self):
        @Typed((int, float), z=bool)
        def f(x, y, z=3):
            return x + y + z
        output = f(1.0, 2)
        self.assertEqual(output, 6)


class TestTypedFunctionIterables(ut.TestCase):

    def test_works_with_tuple_one_type(self):
        @Typed((int, ...))
        def f(x):
            return x
        inp = (1, 2, 3)
        out = f(inp)
        self.assertTupleEqual(out, inp)

    def test_wrong_type_error_with_tuple_one_type(self):
        @Typed((int, ...))
        def f(x):
            return x
        log_msg = ['ERROR:root:Type of element 2 in '
                   'tuple x must be int, not str like foo!',
                   'ERROR:root:An argument of function f defined'
                   f' in module {__name__} is of wrong type!']
        err_msg = ('An argument of function f defined in '
                   f'module {__name__} is of wrong type!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f((1, 2, 'foo'))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_tuple_two_types(self):
        @Typed((int, float, ...))
        def f(x):
            return x
        inp = (1, 2, 3)
        out = f(inp)
        self.assertTupleEqual(out, inp)

    def test_wrong_type_error_with_tuple_two_types(self):
        @Typed((int, float, ...))
        def f(x):
            return x
        log_msg = ["ERROR:root:Type of element 2 in tuple x must "
                   "be one of ('int', 'float'), not str like foo!",
                   'ERROR:root:An argument of function f defined'
                   f' in module {__name__} is of wrong type!']
        err_msg = ('An argument of function f defined in '
                   f'module {__name__} is of wrong type!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f((1, 2, 'foo'))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_not_tuple_error_with_tuple_two_types(self):
        @Typed((int, float, ...))
        def f(x):
            return x
        log_msg = ['ERROR:root:Type of x must be tuple, not str like foo!',
                   'ERROR:root:An argument of function f defined'
                   f' in module {__name__} is of wrong type!']
        err_msg = ('An argument of function f defined in '
                   f'module {__name__} is of wrong type!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f('foo')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_list_one_type(self):
        @Typed([int])
        def f(x):
            return x
        inp = [1, 2, 3]
        out = f(inp)
        self.assertListEqual(out, inp)

    def test_wrong_type_error_with_list_one_type(self):
        @Typed([int])
        def f(x):
            return x
        log_msg = ['ERROR:root:Type of element 2 in '
                   'list x must be int, not str like foo!',
                   'ERROR:root:An argument of function f defined'
                   f' in module {__name__} is of wrong type!']
        err_msg = ('An argument of function f defined in '
                   f'module {__name__} is of wrong type!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f([1, 2, 'foo'])
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_list_two_types(self):
        @Typed([int, float])
        def f(x):
            return x
        inp = [1, 2, 3]
        out = f(inp)
        self.assertListEqual(out, inp)

    def test_wrong_type_error_with_list_two_types(self):
        @Typed([int, float])
        def f(x):
            return x
        log_msg = ["ERROR:root:Type of element 2 in list x must "
                   "be one of ('int', 'float'), not str like foo!",
                   'ERROR:root:An argument of function f defined'
                   f' in module {__name__} is of wrong type!']
        err_msg = ('An argument of function f defined in '
                   f'module {__name__} is of wrong type!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f([1, 2, 'foo'])
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_not_list_error_with_list_two_types(self):
        @Typed([int, float])
        def f(x):
            return x
        log_msg = ['ERROR:root:Type of x must be list, not str like foo!',
                   'ERROR:root:An argument of function f defined'
                   f' in module {__name__} is of wrong type!']
        err_msg = ('An argument of function f defined in '
                   f'module {__name__} is of wrong type!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f('foo')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_set_one_type(self):
        @Typed({int})
        def f(x):
            return x
        inp = {1, 2, 3}
        out = f(inp)
        self.assertSetEqual(out, inp)

    def test_wrong_type_error_with_set_one_type(self):
        @Typed({int})
        def f(x):
            return x
        log_msg = ['ERROR:root:Type of element in '
                   'set x must be int, not str like foo!',
                   'ERROR:root:An argument of function f defined'
                   f' in module {__name__} is of wrong type!']
        err_msg = ('An argument of function f defined in '
                   f'module {__name__} is of wrong type!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f({1, 2, 'foo'})
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_set_two_types(self):
        @Typed({int, float})
        def f(x):
            return x
        inp = {1, 2, 3}
        out = f(inp)
        self.assertSetEqual(out, inp)

    def test_wrong_type_error_with_set_two_types(self):
        @Typed({int, float})
        def f(x):
            return x
        log_msg = ["ERROR:root:Type of element in set x must "
                   "be one of ('int', 'float'), not str like foo!",
                   'ERROR:root:An argument of function f defined'
                   f' in module {__name__} is of wrong type!']
        err_msg = ('An argument of function f defined in '
                   f'module {__name__} is of wrong type!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f({1, 2, 'foo'})
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_not_set_error_with_set_two_types(self):
        @Typed({int, float})
        def f(x):
            return x
        log_msg = ['ERROR:root:Type of x must be set, not str like foo!',
                   'ERROR:root:An argument of function f defined'
                   f' in module {__name__} is of wrong type!']
        err_msg = ('An argument of function f defined in '
                   f'module {__name__} is of wrong type!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f('foo')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_empty_dict(self):
        err_msg = ('Length of dict for type specification'
                   ' of argument 0 must be 1, not 0!')
        with self.assertRaises(LenError) as err:
            @Typed({})
            def f(x):
                return x
        self.assertEqual(str(err.exception), err_msg)

    def test_error_on_dict_too_long(self):
        err_msg = ('Length of dict for type specification'
                   ' of argument x must be 1, not 2!')
        with self.assertRaises(LenError) as err:
            @Typed(x={int: float, str: bool})
            def f(x):
                return x
        self.assertEqual(str(err.exception), err_msg)

    def test_works_with_dict_key_one_type(self):
        @Typed({int: ...})
        def f(x):
            return x
        inp = {1: 'one', 2: True, 3: (3.0,)}
        out = f(inp)
        self.assertDictEqual(out, inp)

    def test_wrong_type_error_with_dict_key_one_type(self):
        @Typed({int: ...})
        def f(x):
            return x
        log_msg = ['ERROR:root:Type of key in dict x'
                   ' must be int, not str like foo!',
                   'ERROR:root:An argument of function f defined'
                   f' in module {__name__} is of wrong type!']
        err_msg = ('An argument of function f defined in '
                   f'module {__name__} is of wrong type!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f({1: 'one', 2: True, 'foo': (3.0,)})
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_dict_key_two_types(self):
        @Typed({(int, float): ...})
        def f(x):
            return x
        inp = {1: 'one', 2: True, 3: (3.0,)}
        out = f(inp)
        self.assertDictEqual(out, inp)

    def test_wrong_type_error_with_dict_key_two_types(self):
        @Typed({(int, float): ...})
        def f(x):
            return x
        log_msg = ["ERROR:root:Type of key in dict x must be "
                   "one of ('int', 'float'), not str like foo!",
                   'ERROR:root:An argument of function f defined'
                   f' in module {__name__} is of wrong type!']
        err_msg = ('An argument of function f defined in '
                   f'module {__name__} is of wrong type!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f({1: 'one', 2: True, 'foo': (3.0,)})
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_not_dict_error_with_dict_key_two_types(self):
        @Typed({(int, float): ...})
        def f(x):
            return x
        log_msg = ['ERROR:root:Type of x must be dict, not str like foo!',
                   'ERROR:root:An argument of function f defined'
                   f' in module {__name__} is of wrong type!']
        err_msg = ('An argument of function f defined in '
                   f'module {__name__} is of wrong type!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f('foo')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_dict_value_one_type(self):
        @Typed({...: str})
        def f(x):
            return x
        inp = {1: 'one', 2: 'two', 3: 'three'}
        out = f(inp)
        self.assertDictEqual(out, inp)

    def test_wrong_type_error_with_dict_value_one_type(self):
        @Typed({...: str})
        def f(x):
            return x
        log_msg = ['ERROR:root:Type of entry 3 in dict '
                   'x must be str, not bool like True!',
                   'ERROR:root:An argument of function f defined'
                   f' in module {__name__} is of wrong type!']
        err_msg = ('An argument of function f defined in '
                   f'module {__name__} is of wrong type!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f({1: 'one', 2: 'two', 3: True})
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_dict_values_two_types(self):
        @Typed({...: (str, int)})
        def f(x):
            return x
        inp = {1: 'one', 2: 'two', 3: 'three'}
        out = f(inp)
        self.assertDictEqual(out, inp)

    def test_wrong_type_error_with_dict_values_two_types(self):
        @Typed({...: (str, int)})
        def f(x):
            return x
        log_msg = ["ERROR:root:Type of entry 3 in dict x must be "
                   "one of ('str', 'int'), not bool like False!",
                   'ERROR:root:An argument of function f defined'
                   f' in module {__name__} is of wrong type!']
        err_msg = ('An argument of function f defined in '
                   f'module {__name__} is of wrong type!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f({1: 'one', 2: 'two', 3: False})
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_not_dict_error_with_dict_values_two_types(self):
        @Typed({...: (str, int)})
        def f(x):
            return x
        log_msg = ['ERROR:root:Type of x must be dict, not str like foo!',
                   'ERROR:root:An argument of function f defined'
                   f' in module {__name__} is of wrong type!']
        err_msg = ('An argument of function f defined in '
                   f'module {__name__} is of wrong type!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f('foo')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_dict_keys_and_values(self):
        @Typed({(int, float): (str, bool)})
        def f(x):
            return x
        inp = {1: 'one', 2: 'two', 3: 'three'}
        out = f(inp)
        self.assertDictEqual(out, inp)


class TestTypedFunctionTypedTuple(ut.TestCase):

    def test_works_with_typed_tuple_one_type(self):
        @Typed(((int,), (str,)))
        def f(x):
            return x
        inp = (1, 'foo')
        out = f(inp)
        self.assertTupleEqual(out, inp)

    def test_wrong_type_error_with_typed_tuple_one_type(self):
        @Typed(((int,), (str,)))
        def f(x):
            return x
        log_msg = ['ERROR:root:Type of element 1 in '
                   'tuple x must be str, not bool like True!',
                   'ERROR:root:An argument of function f defined'
                   f' in module {__name__} is of wrong type!']
        err_msg = ('An argument of function f defined in '
                   f'module {__name__} is of wrong type!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f((1, True))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_typed_tuple_two_types(self):
        @Typed(((int, float), (str, bool)))
        def f(x):
            return x
        inp = (1, 'foo')
        out = f(inp)
        self.assertTupleEqual(out, inp)

    def test_wrong_type_error_with_typed_tuple_two_types(self):
        @Typed(((int, float), (str, bool)))
        def f(x):
            return x
        log_msg = ["ERROR:root:Type of element 0 in tuple x must "
                   "be one of ('int', 'float'), not str like foo!",
                   'ERROR:root:An argument of function f defined'
                   f' in module {__name__} is of wrong type!']
        err_msg = ('An argument of function f defined in '
                   f'module {__name__} is of wrong type!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f(('foo', False))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_not_tuple_error_with_tuple_two_types(self):
        @Typed(((int, float), (str, bool)))
        def f(x):
            return x
        log_msg = ['ERROR:root:Type of x must be tuple, not str like foo!',
                   'ERROR:root:An argument of function f defined'
                   f' in module {__name__} is of wrong type!']
        err_msg = ('An argument of function f defined in '
                   f'module {__name__} is of wrong type!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f('foo')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_length_error_with_tuple_two_types(self):
        @Typed(((int, float), (str, bool)))
        def f(x):
            return x
        log_msg = ['ERROR:root:Length of tuple x must be 2, not 3!',
                   'ERROR:root:An argument of function f defined'
                   f' in module {__name__} is of wrong type!']
        err_msg = ('An argument of function f defined in '
                   f'module {__name__} is of wrong type!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f((1, 'foo', False))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)


class TestTypedMethod(ut.TestCase):

    def test_works_with_methods(self):
        class Test:
            @Typed(int, z=(float, str))
            def m(self, x, y, z=4.0):
                return x + y + z
        t = Test()
        output = t.m(1, 2, 3.0)
        self.assertEqual(output, 6.0)

    def test_error_with_method(self):
        class Test:
            @Typed(int, z=(float, str))
            def m(self, x, y, z=4):
                return x + y + z
        t = Test()
        log_msg = ["ERROR:root:Type of z must be one of "
                   "('float', 'str'), not int like 3!",
                   'ERROR:root:An argument of method m defined'
                   f' in module {__name__} is of wrong type!']
        err_msg = ('An argument of method m defined in '
                   f'module {__name__} is of wrong type!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = t.m(1, 'foo', 3)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)


if __name__ == '__main__':
    ut.main()
