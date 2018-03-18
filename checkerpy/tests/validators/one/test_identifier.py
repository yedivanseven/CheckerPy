import logging
import unittest as ut
from ....validators.one import Identifier
from ....exceptions import IdentifierError, CallableError
from ....functional import CompositionOf


class TestIdentifier(ut.TestCase):

    def test_works_with_sane_identifier(self):
        inp = 'test'
        out = Identifier(inp)
        self.assertEqual(out, inp)

    def test_error_on_unnamed_arg_not_str(self):
        log_msg = ['ERROR:root:1 of type int is not a valid identifier!']
        err_msg = '1 of type int is not a valid identifier!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(IdentifierError) as err:
                _ = Identifier(1)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_arg_not_str(self):
        log_msg = ['ERROR:root:Test of type int is not a valid identifier!']
        err_msg = 'Test of type int is not a valid identifier!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(IdentifierError) as err:
                _ = Identifier(1, 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_unnamed_arg_not_identifier(self):
        log_msg = ['ERROR:root:1 is not a valid identifier!']
        err_msg = '1 is not a valid identifier!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(IdentifierError) as err:
                _ = Identifier('1')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_arg_not_identifier(self):
        log_msg = ['ERROR:root:Test is not a valid identifier!']
        err_msg = 'Test is not a valid identifier!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(IdentifierError) as err:
                _ = Identifier('1', 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_has_attribute_JustStr(self):
        self.assertTrue(hasattr(Identifier, 'JustStr'))

    def test_attribute_JustStr_is_CompositionOf(self):
        self.assertIsInstance(Identifier.JustStr, CompositionOf)

    def test_value_and_name_are_passed_through_JustStr(self):
        log_msg = ['ERROR:root:Test is not a valid identifier!']
        err_msg = 'Test is not a valid identifier!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(IdentifierError) as err:
                _ = Identifier.JustStr('1', 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_has_attribute_o(self):
        self.assertTrue(hasattr(Identifier, 'o'))

    def test_attribute_o_is_callable(self):
        self.assertTrue(callable(Identifier.o))

    def test_o_returns_composition(self):
        def f(x):
            return x
        composition = Identifier.o(f)
        self.assertIsInstance(composition, CompositionOf)

    def test_o_raises_error_on_argument_not_callable(self):
        err_msg = ('foo must be a callable that accepts (i) a value,'
                   ' (ii) an optional name for that value, and (iii)'
                   ' any number of keyword arguments!')
        with self.assertRaises(CallableError) as err:
            _ = Identifier.o('foo')
        self.assertEqual(str(err.exception), err_msg)


if __name__ == '__main__':
    ut.main()
