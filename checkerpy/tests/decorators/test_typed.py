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

    def test_error_on_invalid_type_specification(self):
        err_msg = ('Invalid expression 1 of type int for type specification'
                   ' of argument at position 0! Must be one of type, tuple,'
                   ' list, set, dict, or ellipsis.')
        with self.assertRaises(TypeError) as err:
            @Typed(1)
            def f(x, y):
                return x + y
        self.assertEqual(str(err.exception), err_msg)

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
        log_msg = ['ERROR:root:Type of argument x to function f defined '
                   f'in module {__name__} must be int, not str like foo!']
        err_msg = ('Type of argument x to function f defined in '
                   f'module {__name__} must be int, not str like foo!')
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
        log_msg = ['ERROR:root:Type of argument y to function f defined '
                   f'in module {__name__} must be float, not str like foo!']
        err_msg = ('Type of argument y to function f defined in '
                   f'module {__name__} must be float, not str like foo!')
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
        log_msg = ['ERROR:root:Type of argument y to function f defined '
                   f'in module {__name__} must be float, not str like foo!']
        err_msg = ('Type of argument y to function f defined in '
                   f'module {__name__} must be float, not str like foo!')
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
        log_msg = ["ERROR:root:Type of argument x to function f defined "
                   f"in module {__name__} must be one of ('int', 'float')"
                   ", not str like foo!"]
        err_msg = ("Type of argument x to function f defined in module"
                   f" {__name__} must be one of ('int', 'float'), not "
                   "str like foo!")
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
        log_msg = ["ERROR:root:Type of argument y to function f defined "
                   f"in module {__name__} must be one of ('float', 'complex'),"
                   " not str like foo!"]
        err_msg = ("Type of argument y to function f defined in module"
                   f" {__name__} must be one of ('float', 'complex'), "
                   "not str like foo!")
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
        log_msg = ["ERROR:root:Type of argument y to function f defined "
                   f"in module {__name__} must be one of ('float', 'complex'),"
                   " not str like foo!"]
        err_msg = ("Type of argument y to function f defined in module"
                   f" {__name__} must be one of ('float', 'complex'), "
                   "not str like foo!")
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
        log_msg = ['ERROR:root:Type of argument y to function f defined '
                   f'in module {__name__} must be float, not str like foo!']
        err_msg = ('Type of argument y to function f defined in '
                   f'module {__name__} must be float, not str like foo!')
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
        log_msg = ['ERROR:root:Type of argument y to function f defined '
                   f'in module {__name__} must be float, not str like foo!']
        err_msg = ('Type of argument y to function f defined in '
                   f'module {__name__} must be float, not str like foo!')
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
        log_msg = ['ERROR:root:Type of argument y to function f defined '
                   f'in module {__name__} must be float, not str like foo!']
        err_msg = ('Type of argument y to function f defined in '
                   f'module {__name__} must be float, not str like foo!')
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
        log_msg = ['ERROR:root:Type of argument y to function f defined '
                   f'in module {__name__} must be float, not str like foo!']
        err_msg = ('Type of argument y to function f defined in '
                   f'module {__name__} must be float, not str like foo!')
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

    def test_works_with_required_kwonly_args(self):
        @Typed(int, float, str, z=bool)
        def f(x, y, *, z):
            return x + y + z
        output = f(1, 2.0, z=True)
        self.assertEqual(output, 4.0)

    def test_required_kwonly_args_are_checked(self):
        @Typed(int, float, str)
        def f(x, y, *, z):
            return x + y + z
        log_msg = ['ERROR:root:Type of argument z to function f defined '
                   f'in module {__name__} must be str, not bool like True!']
        err_msg = ('Type of argument z to function f defined in '
                   f'module {__name__} must be str, not bool like True!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f(1, 2.0, z=True)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)


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
        log_msg = ['ERROR:root:Type of argument y to function f defined '
                   f'in module {__name__} must be float, not str like bar!']
        err_msg = ('Type of argument y to function f defined in '
                   f'module {__name__} must be float, not str like bar!')
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
        log_msg = ['ERROR:root:Type of argument y to function f defined '
                   f'in module {__name__} must be float, not str like foo!']
        err_msg = ('Type of argument y to function f defined in '
                   f'module {__name__} must be float, not str like foo!')
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
        log_msg = ['ERROR:root:Type of argument y to function f defined '
                   f'in module {__name__} must be float, not str like foo!']
        err_msg = ('Type of argument y to function f defined in '
                   f'module {__name__} must be float, not str like foo!')
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
        log_msg = ["ERROR:root:Type of argument y to function f defined "
                   f"in module {__name__} must be one of ('int', 'float'),"
                   " not str like bar!"]
        err_msg = ("Type of argument y to function f defined in module"
                   f" {__name__} must be one of ('int', 'float'), not "
                   "str like bar!")
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
        log_msg = ["ERROR:root:Type of argument y to function f defined in"
                   f" module {__name__} must be one of ('int', 'float'), "
                   "not str like foo!"]
        err_msg = ("Type of argument y to function f defined in module"
                   f" {__name__} must be one of ('int', 'float'), "
                   "not str like foo!")
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
        log_msg = ["ERROR:root:Type of argument y to function f defined "
                   f"in module {__name__} must be one of ('int', 'float')"
                   ", not str like foo!"]
        err_msg = ("Type of argument y to function f defined in module"
                   f" {__name__} must be one of ('int', 'float'), not "
                   "str like foo!")
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
        log_msg = ['ERROR:root:Type of argument y to function f defined '
                   f'in module {__name__} must be float, not str like foo!']
        err_msg = ('Type of argument y to function f defined in '
                   f'module {__name__} must be float, not str like foo!')
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
        log_msg = ['ERROR:root:Type of argument x to function f defined '
                   f'in module {__name__} must be float, not str like foo!']
        err_msg = ('Type of argument x to function f defined in '
                   f'module {__name__} must be float, not str like foo!')
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
        log_msg = ['ERROR:root:Type of argument x to function f defined '
                   f'in module {__name__} must be float, not str like foo!']
        err_msg = ('Type of argument x to function f defined in '
                   f'module {__name__} must be float, not str like foo!')
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
        log_msg = ["ERROR:root:Type of argument y to function f defined "
                   f"in module {__name__} must be one of ('int', 'str'),"
                   " not float like 2.0!"]
        err_msg = ("Type of argument y to function f defined in "
                   f"module {__name__} must be one of ('int', 'str'),"
                   " not float like 2.0!")
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
        log_msg = ['ERROR:root:Type of argument z to function f defined '
                   f'in module {__name__} must be str, not bool like False!']
        err_msg = ('Type of argument z to function f defined in '
                   f'module {__name__} must be str, not bool like False!')
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
        log_msg = ["ERROR:root:Type of argument u to function f defined "
                   f"in module {__name__} must be one of ('int', 'str'),"
                   " not float like 4.0!"]
        err_msg = ("Type of argument u to function f defined in module"
                   f" {__name__} must be one of ('int', 'str'), not "
                   "float like 4.0!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f(1.0, 'foo', 'bar', 4.0, 5.0)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_kwarg_types_take_precedence_over_arg_types(self):
        @Typed(int, float, bool, z=str)
        def f(x, y, z):
            return x + y + z
        log_msg = ['ERROR:root:Type of argument z to function f defined '
                   f'in module {__name__} must be str, not bool like True!']
        err_msg = ('Type of argument z to function f defined in '
                   f'module {__name__} must be str, not bool like True!')
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
        log_msg = ['ERROR:root:Type of argument z to function f defined '
                   f'in module {__name__} must be str, not bool like True!']
        err_msg = ('Type of argument z to function f defined in '
                   f'module {__name__} must be str, not bool like True!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f(1, 2.0, True)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_arg_and_kwarg_types_and_ellipsis(self):
        @Typed(..., bool, z=(float, tuple))
        def f(x, y, z):
            return x + y + z
        output = f(1, True, 2.0)
        self.assertEqual(output, 4.0)

    def test_error_with_arg_and_kwarg_types_and_ellipsis(self):
        @Typed(int, ..., z=(float, tuple))
        def f(x, y, z):
            return x + y + z
        log_msg = ["ERROR:root:Type of argument z to function f defined "
                   f"in module {__name__} must be one of ('float', 'tuple'),"
                   " not bool like True!"]
        err_msg = ("Type of argument z to function f defined in module"
                   f" {__name__} must be one of ('float', 'tuple'), "
                   "not bool like True!")
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

    def test_error_on_overriding_defaults_with_arg(self):
        @Typed(y=(int, float), z=str)
        def f(x, y, z=3):
            return x + y + z
        log_msg = ['ERROR:root:Type of argument z to function f defined '
                   f'in module {__name__} must be str, not bool like True!']
        err_msg = ('Type of argument z to function f defined in '
                   f'module {__name__} must be str, not bool like True!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f(1, 2.0, True)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_overriding_defaults_with_kwarg(self):
        @Typed(y=(int, float), z=str)
        def f(x, y, z=3):
            return x + y + z
        log_msg = ['ERROR:root:Type of argument z to function f defined '
                   f'in module {__name__} must be str, not bool like True!']
        err_msg = ('Type of argument z to function f defined in '
                   f'module {__name__} must be str, not bool like True!')
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


class TestTypedFunctionsIterables(ut.TestCase):

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
        log_msg = ['ERROR:root:Type of element 2 in tuple argument x '
                   f'to function f defined in module {__name__} must '
                   'be int, not str like foo!']
        err_msg = ('Type of element 2 in tuple argument x to function f def'
                   f'ined in module {__name__} must be int, not str like foo!')
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
        log_msg = ["ERROR:root:Type of element 2 in tuple argument x "
                   f"to function f defined in module {__name__} must"
                   " be one of ('int', 'float'), not str like foo!"]
        err_msg = ("Type of element 2 in tuple argument x to function f "
                   f"defined in module {__name__} must be one of ('int',"
                   " 'float'), not str like foo!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f((1, 2, 'foo'))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_not_tuple_error_with_tuple_two_types(self):
        @Typed((int, float, ...))
        def f(x):
            return x
        log_msg = ['ERROR:root:Type of argument x to function f defined '
                   f'in module {__name__} must be tuple, not str like foo!']
        err_msg = ('Type of argument x to function f defined in '
                   f'module {__name__} must be tuple, not str like foo!')
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
        log_msg = ['ERROR:root:Type of element 2 in list argument x '
                   f'to function f defined in module {__name__} must'
                   ' be int, not str like foo!']
        err_msg = ('Type of element 2 in list argument x to function f def'
                   f'ined in module {__name__} must be int, not str like foo!')
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
        log_msg = ["ERROR:root:Type of element 2 in list argument x "
                   f"to function f defined in module {__name__} must"
                   " be one of ('int', 'float'), not str like foo!"]
        err_msg = ("Type of element 2 in list argument x to function f"
                   f" defined in module {__name__} must be one of ('int',"
                   " 'float'), not str like foo!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f([1, 2, 'foo'])
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_not_list_error_with_list_two_types(self):
        @Typed([int, float])
        def f(x):
            return x
        log_msg = ["ERROR:root:Type of argument x to function f defined in"
                   f" module {__name__} must be one of ('list', 'deque'), "
                   "not str like foo!"]
        err_msg = ("Type of argument x to function f defined in"
                   f" module {__name__} must be one of ('list', 'deque'),"
                   " not str like foo!")
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
        log_msg = ['ERROR:root:Type of element in set argument x to'
                   f' function f defined in module {__name__} must '
                   'be int, not str like foo!']
        err_msg = ('Type of element in set argument x to function f defined'
                   f' in module {__name__} must be int, not str like foo!')
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
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f({1, 2, 'foo'})

    def test_not_set_error_with_set_two_types(self):
        @Typed({int, float})
        def f(x):
            return x
        log_msg = ["ERROR:root:Type of argument x to function f defined in "
                   f"module {__name__} must be one of ('set', 'frozenset'),"
                   " not str like foo!"]
        err_msg = ("Type of argument x to function f defined in "
                   f"module {__name__} must be one of ('set', 'frozenset'),"
                   " not str like foo!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f('foo')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_empty_dict(self):
        log_msg = ['ERROR:root:Length of dict for type specification'
                   ' of argument at position 0 must be 1, not 0!']
        err_msg = ('Length of dict for type specification of '
                   'argument at position 0 must be 1, not 0!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                @Typed({})
                def f(x):
                    return x
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_dict_too_long(self):
        log_msg = ['ERROR:root:Length of dict for type specification'
                   ' of argument x must be 1, not 2!']
        err_msg = ('Length of dict for type specification'
                   ' of argument x must be 1, not 2!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                @Typed(x={int: float, str: bool})
                def f(x):
                    return x
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

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
        log_msg = ['ERROR:root:Type of key in dict argument x to '
                   f'function f defined in module {__name__} must'
                   ' be int, not str like foo!']
        err_msg = ('Type of key in dict argument x to function f defined '
                   f'in module {__name__} must be int, not str like foo!')
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
        log_msg = ["ERROR:root:Type of key in dict argument x to function f "
                   f"defined in module {__name__} must be one of ('int', "
                   "'float'), not str like foo!"]
        err_msg = ("Type of key in dict argument x to function f defined "
                   f"in module {__name__} must be one of ('int', 'float')"
                   ", not str like foo!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f({1: 'one', 2: True, 'foo': (3.0,)})
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_not_dict_error_with_dict_key_two_types(self):
        @Typed({(int, float): ...})
        def f(x):
            return x
        log_msg = ["ERROR:root:Type of argument x to function f defined in "
                   f"module {__name__} must be one of ('dict', 'defaultdict',"
                   " 'OrderedDict'), not str like foo!"]
        err_msg = ("Type of argument x to function f defined in module "
                   f"{__name__} must be one of ('dict', 'defaultdict',"
                   " 'OrderedDict'), not str like foo!")
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
        log_msg = ['ERROR:root:Type of entry 3 in dict argument x '
                   f'to function f defined in module {__name__} must'
                   ' be str, not bool like True!']
        err_msg = ('Type of entry 3 in dict argument x to function f defined'
                   f' in module {__name__} must be str, not bool like True!')
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
        log_msg = ["ERROR:root:Type of entry 3 in dict argument x "
                   f"to function f defined in module {__name__} must "
                   "be one of ('str', 'int'), not bool like False!"]
        err_msg = ("Type of entry 3 in dict argument x to function f defined"
                   f" in module {__name__} must be one of ('str', 'int'), "
                   "not bool like False!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f({1: 'one', 2: 'two', 3: False})
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_not_dict_error_with_dict_values_two_types(self):
        @Typed({...: (str, int)})
        def f(x):
            return x
        log_msg = ["ERROR:root:Type of argument x to function f defined in "
                   f"module {__name__} must be one of ('dict', 'defaultdict',"
                   " 'OrderedDict'), not str like foo!"]
        err_msg = ("Type of argument x to function f defined in module "
                   f"{__name__} must be one of ('dict', 'defaultdict', "
                   "'OrderedDict'), not str like foo!")
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


class TestTypedFunctionsTypedTuple(ut.TestCase):

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
        log_msg = ['ERROR:root:Type of element 1 in tuple argument x'
                   f' to function f defined in module {__name__} must'
                   ' be str, not bool like True!']
        err_msg = ('Type of element 1 in tuple argument x to function f'
                   f' defined in module {__name__} must be str, not bool'
                   ' like True!')
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
        log_msg = ["ERROR:root:Type of element 0 in tuple argument x"
                   f" to function f defined in module {__name__} must"
                   " be one of ('int', 'float'), not str like foo!"]
        err_msg = ("Type of element 0 in tuple argument x to function f"
                   f" defined in module {__name__} must be one of ('int',"
                   " 'float'), not str like foo!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f(('foo', False))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_typed_tuple_two_types_ellipsis(self):
        @Typed(((...,), (str, bool)))
        def f(x):
            return x
        inp = (1, 'foo')
        out = f(inp)
        self.assertTupleEqual(out, inp)

    def test_wrong_type_error_with_typed_tuple_two_types_ellipsis(self):
        @Typed(((int, float), (...,)))
        def f(x):
            return x
        log_msg = ["ERROR:root:Type of element 0 in tuple argument x"
                   f" to function f defined in module {__name__} must"
                   " be one of ('int', 'float'), not str like foo!"]
        err_msg = ("Type of element 0 in tuple argument x to function f"
                   f" defined in module {__name__} must be one of ('int',"
                   " 'float'), not str like foo!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f(('foo', False))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_not_tuple_error_with_tuple_two_types(self):
        @Typed(((int, float), (str, bool)))
        def f(x):
            return x
        log_msg = ['ERROR:root:Type of argument x to function f defined '
                   f'in module {__name__} must be tuple, not str like foo!']
        err_msg = ('Type of argument x to function f defined in '
                   f'module {__name__} must be tuple, not str like foo!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f('foo')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_length_error_with_tuple_two_types(self):
        @Typed(((int, float), (str, bool)))
        def f(x):
            return x
        log_msg = ['ERROR:root:Length of tuple argument x to function f'
                   f' defined in module {__name__} must be 2, not 3!']
        err_msg = ('Length of tuple argument x to function f defined'
                   f' in module {__name__} must be 2, not 3!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = f((1, 'foo', False))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)


class TestTypedMethods(ut.TestCase):

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
        log_msg = ["ERROR:root:Type of argument z to method m defined"
                   f" in module {__name__} must be one of ('float', "
                   "'str'), not int like 3!"]
        err_msg = ("Type of argument z to method m defined in module"
                   f" {__name__} must be one of ('float', 'str'),"
                   " not int like 3!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = t.m(1, 'foo', 3)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)


if __name__ == '__main__':
    ut.main()
