import logging
import unittest as ut
from ...decorators import Typed
from ...exceptions import WrongTypeError


class TestTypedFunctionsArgTypes(ut.TestCase):

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

    def test_works_with_no_types(self):
        @Typed()
        def f(x, y):
            return x + y
        output = f(1, 2.0)
        self.assertEqual(output, 3.0)

    def test_works_with_two_arg_types_no_args(self):
        @Typed((int, float), str)
        def f():
            return 3.0
        output = f()
        self.assertEqual(output, 3.0)

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

    def test_works_with_optional_args_and_kwargs(self):
        @Typed((int, str), float)
        def f(x, y, *args, **kwargs):
            return x + y + sum(args) + kwargs['z']
        output = f(1, 2.0, 3, 4, z=5)
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


class TestTypedFunctionsKwargTypes(ut.TestCase):

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

    def test_works_with_singla_kwarg_type_no_args(self):
        @Typed(y=float, z=str)
        def f():
            return 3.0
        output = f()
        self.assertEqual(output, 3.0)

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

    def test_error_with_two_arg_types_too_many_types(self):
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

    def test_works_with_mixed_kwarg_types_too_few_types(self):
        @Typed(z=(int, str), y=float)
        def f(x, y, z):
            return x + y + z
        output = f(1, 2.0, 3)
        self.assertEqual(output, 6.0)

    def test_error_with_mixed_arg_types_too_few_types(self):
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

    def test_works_with_two_kwarg_types_no_args(self):
        @Typed(y=(int, float), z=str)
        def f():
            return 3.0
        output = f()
        self.assertEqual(output, 3.0)

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

    def test_error_on_defaults(self):
        @Typed(y=(int, str), z=float)
        def f(x, y, z=3):
            return x + y + z
        log_msg = ["ERROR:root:Type of y must be one of "
                   "('int', 'str'), not float like 2.0!",
                   'ERROR:root:An argument of function f defined'
                   f' in module {__name__} is of wrong type!']
        err_msg = ('An argument of function f defined in '
                   f'module {__name__} is of wrong type!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f(1, 2.0)
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
