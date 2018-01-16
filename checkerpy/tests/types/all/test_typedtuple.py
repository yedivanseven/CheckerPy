import logging
import unittest as ut
from ....functional import CompositionOf
from ....types.all import TypedTuple
from ....exceptions import LenError, WrongTypeError


class TestTypedTuple(ut.TestCase):

    def test_works_with_empty_tuple(self):
        out = TypedTuple(())
        self.assertTupleEqual(out, ())

    def test_error_on_type_spec_no_length(self):
        err_msg = ("Length of types argument 2 with"
                   " type int cannot be determined!")
        with self.assertRaises(LenError) as err:
            _ = TypedTuple((1,), types=2)
        self.assertEqual(str(err.exception), err_msg)

    def test_error_on_type_spec_wrong_type(self):
        err_msg = 'Type of type specifier 2 must be type, not int!'
        with self.assertRaises(TypeError) as err:
            _ = TypedTuple((1,), types=[2])
        self.assertEqual(str(err.exception), err_msg)

    def test_works_with_single_type_for_each_element(self):
        inp = (1, 'foo', True)
        out = TypedTuple(inp, types=[int, str, bool])
        self.assertTupleEqual(out, inp)

    def test_works_with_single_type_for_each_element_as_tuple(self):
        inp = (1, 'foo', True)
        out = TypedTuple(inp, types=[(int,), (str,), (bool,)])
        self.assertTupleEqual(out, inp)

    def test_works_with_multiple_types_for_each_element(self):
        inp = (1, 'foo', True)
        out = TypedTuple(inp, types=[(int, float), (str, tuple), (bool, list)])
        self.assertTupleEqual(out, inp)

    def test_error_on_unnamed_tuple_wrong_length(self):
        inp = (1, 'foo', True)
        log_msg = ["ERROR:root:Length of tuple (1, "
                   "'foo', True) must be 2, not 3!"]
        err_msg = "Length of tuple (1, 'foo', True) must be 2, not 3!"
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = TypedTuple(inp, types=(int, str))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_tuple_wrong_length(self):
        inp = (1, 'foo', True)
        log_msg = ['ERROR:root:Length of tuple test must be 2, not 3!']
        err_msg = 'Length of tuple test must be 2, not 3!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(LenError) as err:
                _ = TypedTuple(inp, 'test', types=(int, str))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_wrong_unnamed_tuple_element_single_type(self):
        inp = (1, 'foo', True)
        log_msg = ["ERROR:root:Type of element 1 in tuple (1, 'foo',"
                   " True) must be float, not str like foo!"]
        err_msg = ("Type of element 1 in tuple (1, 'foo', True)"
                   " must be float, not str like foo!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = TypedTuple(inp, types=(int, float, bool))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_wrong_named_tuple_element_single_type(self):
        inp = (1, 'foo', True)
        log_msg = ['ERROR:root:Type of element 1 in tuple '
                   'test must be float, not str like foo!']
        err_msg = ('Type of element 1 in tuple test '
                   'must be float, not str like foo!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = TypedTuple(inp, 'test', types=(int, float, bool))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_wrong_unnamed_tuple_element_multiple_types(self):
        inp = (1, 'foo', True)
        log_msg = ["ERROR:root:Type of element 1 in tuple (1, 'foo', True)"
                   " must be one of ('int', 'float'), not str like foo!"]
        err_msg = ("Type of element 1 in tuple (1, 'foo', True) must"
                   " be one of ('int', 'float'), not str like foo!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = TypedTuple(inp, types=(int, (int, float), bool))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_wrong_named_tuple_element_multiple_types(self):
        inp = (1, 'foo', True)
        log_msg = ["ERROR:root:Type of element 1 in tuple test must"
                   " be one of ('int', 'float'), not str like foo!"]
        err_msg = ("Type of element 1 in tuple test must be one"
                   " of ('int', 'float'), not str like foo!")
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(WrongTypeError) as err:
                _ = TypedTuple(inp, 'test', types=(int, (int, float), bool))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_has_attribute_o(self):
        self.assertTrue(hasattr(TypedTuple, 'o'))

    def test_attribute_o_is_callable(self):
        self.assertTrue(callable(TypedTuple.o))

    def test_o_returns_composition(self):
        def f(x):
            return x
        composition = TypedTuple.o(f)
        self.assertIsInstance(composition, CompositionOf)


if __name__ == '__main__':
    ut.main()
