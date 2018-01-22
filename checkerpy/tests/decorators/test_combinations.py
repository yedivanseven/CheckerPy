import logging
import unittest as ut
from ...decorators import Typed, Bounded
from ...exceptions import WrongTypeError, LimitError


class TestTypedOnTyped(ut.TestCase):

    def test_works(self):
        @Typed(int, ..., w=str)
        @Typed(..., float, v=bool)
        def f(x, y, v, w):
            return x + y + v, w
        out_num, out_str = f(1, 2.0, True, 'test')
        self.assertEqual(out_num, 4.0)
        self.assertEqual(out_str, 'test')

    def test_catches_wrong_arg_type(self):
        @Typed(int, ..., w=str)
        @Typed(..., float, v=bool)
        def f(x, y, v, w):
            return x + y + v, w
        log_msg = ['ERROR:root:Type of argument x to function f defined '
                   f'in module {__name__} must be int, not str like foo!']
        err_msg = ('Type of argument x to function f defined in module'
                   f' {__name__} must be int, not str like foo!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f('foo', 2.0, v=True, w='test')
        self.assertEqual(log.output, log_msg)
        self.assertEqual(str(err.exception), err_msg)

    def test_catches_wrong_kwarg_type(self):
        @Typed(int, ..., w=str)
        @Typed(..., float, v=bool)
        def f(x, y, v, w):
            return x + y + v, w
        log_msg = ['ERROR:root:Type of argument w to function f defined '
                   f'in module {__name__} must be str, not bool like False!']
        err_msg = ('Type of argument w to function f defined in module'
                   f' {__name__} must be str, not bool like False!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f(1, 2.0, v=True, w=False)
        self.assertEqual(log.output, log_msg)
        self.assertEqual(str(err.exception), err_msg)

    def test_second_overrides_first_arg_type(self):
        @Typed(int, int, w=str)
        @Typed(..., float, v=bool)
        def f(x, y, v, w):
            return x + y + v, w
        log_msg = ['ERROR:root:Type of argument y to function f defined '
                   f'in module {__name__} must be int, not float like 2.0!']
        err_msg = ('Type of argument y to function f defined in module'
                   f' {__name__} must be int, not float like 2.0!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f(1, 2.0, v=True, w='test')
        self.assertEqual(log.output, log_msg)
        self.assertEqual(str(err.exception), err_msg)

    def test_second_overrides_first_kwarg_type(self):
        @Typed(int, int, v=str)
        @Typed(..., float, v=bool)
        def f(x, y, v, w):
            return x + y + v, w
        log_msg = ['ERROR:root:Type of argument v to function f defined '
                   f'in module {__name__} must be str, not bool like True!']
        err_msg = ('Type of argument v to function f defined in module'
                   f' {__name__} must be str, not bool like True!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f(1, 2.0, v=True, w='test')
        self.assertEqual(log.output, log_msg)
        self.assertEqual(str(err.exception), err_msg)


class TestBoundedOnBounded(ut.TestCase):

    def test_works(self):
        @Bounded((1, 2), ..., w=(7, 8))
        @Bounded(..., (3, 4), v=(5, 6))
        def f(x, y, v, w):
            return x + y + v + w
        output = f(1, 3, v=5, w=7)
        self.assertEqual(output, 16)

    def test_catches_wrong_arg_limit(self):
        @Bounded((1, 2), ..., w=(7, 8))
        @Bounded(..., (3, 4), v=(5, 6))
        def f(x, y, v, w):
            return x + y + v + w
        log_msg = ['ERROR:root:Value 3 of argument x to function '
                   f'f defined in module {__name__} lies outside '
                   f'the allowed interval [1, 2]!']
        err_msg = ('Value 3 of argument x to function f defined in module '
                   f'{__name__} lies outside the allowed interval [1, 2]!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LimitError) as err:
                _ = f(3, 3, v=5, w=7)
        self.assertEqual(log.output, log_msg)
        self.assertEqual(str(err.exception), err_msg)

    def test_catches_wrong_kwarg_limit(self):
        @Bounded((1, 2), ..., w=(7, 8))
        @Bounded(..., (3, 4), v=(5, 6))
        def f(x, y, v, w):
            return x + y + v + w
        log_msg = ['ERROR:root:Value 5 of argument w to function '
                   f'f defined in module {__name__} lies outside '
                   f'the allowed interval [7, 8]!']
        err_msg = ('Value 5 of argument w to function f defined in module '
                   f'{__name__} lies outside the allowed interval [7, 8]!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LimitError) as err:
                _ = f(1, 3, v=5, w=5)
        self.assertEqual(log.output, log_msg)
        self.assertEqual(str(err.exception), err_msg)

    def test_second_overrides_first_arg_limit(self):
        @Bounded((1, 2), (1, 2), w=(7, 8))
        @Bounded(..., (3, 4), v=(5, 6))
        def f(x, y, v, w):
            return x + y + v + w
        log_msg = ['ERROR:root:Value 3 of argument y to function '
                   f'f defined in module {__name__} lies outside '
                   f'the allowed interval [1, 2]!']
        err_msg = ('Value 3 of argument y to function f defined in module '
                   f'{__name__} lies outside the allowed interval [1, 2]!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LimitError) as err:
                _ = f(1, 3, v=5, w=7)
        self.assertEqual(log.output, log_msg)
        self.assertEqual(str(err.exception), err_msg)

    def test_second_overrides_first_kwarg_limit(self):
        @Bounded((1, 2), ..., v=(7, 8))
        @Bounded(..., (3, 4), v=(5, 6))
        def f(x, y, v, w):
            return x + y + v + w
        log_msg = ['ERROR:root:Value 5 of argument v to function '
                   f'f defined in module {__name__} lies outside '
                   f'the allowed interval [7, 8]!']
        err_msg = ('Value 5 of argument v to function f defined in module '
                   f'{__name__} lies outside the allowed interval [7, 8]!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LimitError) as err:
                _ = f(1, 3, 5, w='test')
        self.assertEqual(log.output, log_msg)
        self.assertEqual(str(err.exception), err_msg)


class TestBoundedOnTyped(ut.TestCase):

    def test_works(self):
        @Bounded((1, 2), w=(3, 4))
        @Typed(int, float, v=int)
        def f(x, y, v, w):
            return x + y + v + w
        output = f(1, 2.0, w=4, v=3)
        self.assertEqual(output, 10.0)

    def test_catches_wrong_arg_limit(self):
        @Bounded((1, 2), w=(3, 4))
        @Typed(int, float, v=int)
        def f(x, y, v, w):
            return x + y + v + w
        log_msg = ['ERROR:root:Value 3 of argument x to function '
                   f'f defined in module {__name__} lies outside '
                   f'the allowed interval [1, 2]!']
        err_msg = ('Value 3 of argument x to function f defined in module '
                   f'{__name__} lies outside the allowed interval [1, 2]!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LimitError) as err:
                _ = f(3, 2.0, w=4, v=3)
        self.assertEqual(log.output, log_msg)
        self.assertEqual(str(err.exception), err_msg)

    def test_catches_wrong_kwarg_limit(self):
        @Bounded((1, 2), w=(3, 4))
        @Typed(int, float, v=int)
        def f(x, y, v, w):
            return x + y + v + w
        log_msg = ['ERROR:root:Value 5 of argument w to function '
                   f'f defined in module {__name__} lies outside '
                   f'the allowed interval [3, 4]!']
        err_msg = ('Value 5 of argument w to function f defined in module '
                   f'{__name__} lies outside the allowed interval [3, 4]!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LimitError) as err:
                _ = f(1, 3, w=5, v=4)
        self.assertEqual(log.output, log_msg)
        self.assertEqual(str(err.exception), err_msg)


class TestTypedOnBounded(ut.TestCase):

    def test_works(self):
        @Typed(int, float, w=int)
        @Bounded((1, 2), v=(3, 4))
        def f(x, y, v, w):
            return x + y + v + w
        output = f(1, 2.0, w=4, v=3)
        self.assertEqual(output, 10.0)

    def test_catches_wrong_arg_type(self):
        @Typed(int, float, w=int)
        @Bounded((1, 2), v=(3, 4))
        def f(x, y, v, w):
            return x + y + v + w
        log_msg = ['ERROR:root:Type of argument y to function f defined '
                   f'in module {__name__} must be float, not int like 2!']
        err_msg = ('Type of argument y to function f defined in module'
                   f' {__name__} must be float, not int like 2!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f(1, 2, w=4, v=3.0)
        self.assertEqual(log.output, log_msg)
        self.assertEqual(str(err.exception), err_msg)

    def test_catches_wrong_kwarg_type(self):
        @Typed(int, float, w=int)
        @Bounded((1, 2), v=(3, 4))
        def f(x, y, v, w):
            return x + y + v + w
        log_msg = ['ERROR:root:Type of argument w to function f defined '
                   f'in module {__name__} must be int, not float like 4.0!']
        err_msg = ('Type of argument w to function f defined in module'
                   f' {__name__} must be int, not float like 4.0!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = f(1, 2.0, w=4.0, v=3)
        self.assertEqual(log.output, log_msg)
        self.assertEqual(str(err.exception), err_msg)


if __name__ == '__main__':
    ut.main()
