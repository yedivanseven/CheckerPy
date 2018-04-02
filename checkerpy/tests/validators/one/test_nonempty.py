import logging
import unittest as ut
from ....validators.one import NonEmpty
from ....exceptions import EmptyError, CallableError
from ....types.one import _ITERABLES
from ....types.weak import _LIKE_ITERABLES
from ....functional import CompositionOf


class TestNonEmpty(ut.TestCase):

    def test_error_on_invalid_unnamed_argument(self):
        log_msg = ['ERROR:root:Emptiness of 1 with '
                   'type int cannot be determined!']
        err_msg = 'Emptiness of 1 with type int cannot be determined!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(EmptyError) as err:
                _ = NonEmpty(1)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_invalid_named_argument(self):
        log_msg = ['ERROR:root:Emptiness of test with '
                   'type float cannot be determined!']
        err_msg = 'Emptiness of test with type float cannot be determined!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(EmptyError) as err:
                _ = NonEmpty(2.0, 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_sane_string(self):
        out = NonEmpty('foo')
        self.assertIsInstance(out, str)
        self.assertEqual(out, 'foo')

    def test_error_on_empty_unnamed_str(self):
        log_msg = ['ERROR:root:Str must not be empty!']
        err_msg = 'Str must not be empty!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(EmptyError) as err:
                _ = NonEmpty('')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_empty_named_str(self):
        log_msg = ['ERROR:root:Str test must not be empty!']
        err_msg = 'Str test must not be empty!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(EmptyError) as err:
                _ = NonEmpty('', 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_sane_tuple(self):
        out = NonEmpty((1,))
        self.assertIsInstance(out, tuple)
        self.assertTupleEqual(out, (1,))

    def test_error_on_empty_unnamed_tuple(self):
        log_msg = ['ERROR:root:Tuple must not be empty!']
        err_msg = 'Tuple must not be empty!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(EmptyError) as err:
                _ = NonEmpty(())
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_empty_named_tuple(self):
        log_msg = ['ERROR:root:Tuple test must not be empty!']
        err_msg = 'Tuple test must not be empty!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(EmptyError) as err:
                _ = NonEmpty((), 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_sane_list(self):
        out = NonEmpty([2])
        self.assertIsInstance(out, list)
        self.assertListEqual(out, [2])

    def test_error_on_empty_unnamed_list(self):
        log_msg = ['ERROR:root:List must not be empty!']
        err_msg = 'List must not be empty!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(EmptyError) as err:
                _ = NonEmpty([])
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_empty_named_list(self):
        log_msg = ['ERROR:root:List test must not be empty!']
        err_msg = 'List test must not be empty!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(EmptyError) as err:
                _ = NonEmpty([], 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_sane_set(self):
        out = NonEmpty({3})
        self.assertIsInstance(out, set)
        self.assertSetEqual(out, {3})

    def test_error_on_empty_unnamed_set(self):
        log_msg = ['ERROR:root:Set must not be empty!']
        err_msg = 'Set must not be empty!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(EmptyError) as err:
                _ = NonEmpty(set())
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_empty_named_set(self):
        log_msg = ['ERROR:root:Set test must not be empty!']
        err_msg = 'Set test must not be empty!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(EmptyError) as err:
                _ = NonEmpty(set(), 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_sane_dict(self):
        out = NonEmpty({4: 'four'})
        self.assertIsInstance(out, dict)
        self.assertDictEqual(out, {4: 'four'})

    def test_error_on_empty_unnamed_dict(self):
        log_msg = ['ERROR:root:Dict must not be empty!']
        err_msg = 'Dict must not be empty!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(EmptyError) as err:
                _ = NonEmpty({})
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_empty_named_dict(self):
        log_msg = ['ERROR:root:Dict test must not be empty!']
        err_msg = 'Dict test must not be empty!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(EmptyError) as err:
                _ = NonEmpty({}, 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_sane_dictkeys(self):
        inp = {4: 'four'}.keys()
        out = NonEmpty(inp)
        self.assertIsInstance(out, type(inp))
        self.assertEqual(out, inp)

    def test_error_on_empty_unnamed_dictkeys(self):
        log_msg = ['ERROR:root:Dict_keys must not be empty!']
        err_msg = 'Dict_keys must not be empty!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(EmptyError) as err:
                _ = NonEmpty({}.keys())
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_empty_named_dictkeys(self):
        log_msg = ['ERROR:root:Dict_keys test must not be empty!']
        err_msg = 'Dict_keys test must not be empty!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(EmptyError) as err:
                _ = NonEmpty({}.keys(), 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_works_with_sane_frozenset(self):
        inp = frozenset([1, 2])
        out = NonEmpty(inp)
        self.assertIsInstance(out, type(inp))
        self.assertEqual(out, inp)

    def test_error_on_empty_unnamed_frozenset(self):
        log_msg = ['ERROR:root:Frozenset must not be empty!']
        err_msg = 'Frozenset must not be empty!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(EmptyError) as err:
                _ = NonEmpty(frozenset([]))
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_empty_named_frozenset(self):
        log_msg = ['ERROR:root:Frozenset test must not be empty!']
        err_msg = 'Frozenset test must not be empty!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(EmptyError) as err:
                _ = NonEmpty(frozenset([]), 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)


class TestOneOfMethods(ut.TestCase):

    def test_has_iterable_type_checker_attributes(self):
        for iterable in _ITERABLES:
            self.assertTrue(hasattr(NonEmpty, iterable.__name__))
        for iterable in _LIKE_ITERABLES:
            self.assertTrue(hasattr(NonEmpty, iterable.__name__))
        self.assertTrue(hasattr(NonEmpty, 'LikeSized'))

    def test_iterable_type_checkers_are_type_CompositionOf(self):
        for iterable in _ITERABLES:
            type_checker = getattr(NonEmpty, iterable.__name__)
            self.assertIsInstance(type_checker, CompositionOf)
        for iterable in _LIKE_ITERABLES:
            type_checker = getattr(NonEmpty, iterable.__name__)
            self.assertIsInstance(type_checker, CompositionOf)
        sized_checker = getattr(NonEmpty, 'LikeSized')
        self.assertIsInstance(sized_checker, CompositionOf)

    def test_works_through_type_checker(self):
        log_msg = ['ERROR:root:Tuple test must not be empty!']
        err_msg = 'Tuple test must not be empty!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(EmptyError) as err:
                _ = NonEmpty.JustTuple((), 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_has_attribute_o(self):
        self.assertTrue(hasattr(NonEmpty, 'o'))

    def test_attribute_o_is_callable(self):
        self.assertTrue(callable(NonEmpty.o))

    def test_o_returns_composition(self):
        def f(x):
            return x
        composition = NonEmpty.o(f)
        self.assertIsInstance(composition, CompositionOf)

    def test_o_raises_error_on_argument_not_callable(self):
        err_msg = ('foo must be a callable that accepts (i) a value,'
                   ' (ii) an optional name for that value, and (iii)'
                   ' any number of keyword arguments!')
        with self.assertRaises(CallableError) as err:
            _ = NonEmpty.o('foo')
        self.assertEqual(str(err.exception), err_msg)


if __name__ == '__main__':
    ut.main()
