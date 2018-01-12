import unittest as ut
from ...functional import CompositionOf
from ...exceptions import CallableError


class TestCompositionOfInstantiation(ut.TestCase):

    def setUp(self):
        self.f = lambda x, name=None: x^2
        self.g = lambda y, name=None: y - 3

    def test_works_with_sane_callables(self):
        _ = CompositionOf(self.f, self.g)

    def test_error_on_first_arg_not_callable(self):
        wrong_callable = 'Foo'
        err_msg = (f'{wrong_callable} must be a callable that accepts'
                   ' (i) a value, (ii) an optional name for that value,'
                   ' and (iii) any number of keyword arguments!')
        with self.assertRaises(CallableError) as err:
            _ = CompositionOf(wrong_callable, self.g)
        self.assertEqual(str(err.exception), err_msg)

    def test_error_on_second_arg_not_callable(self):
        wrong_callable = 'Bar'
        err_msg = (f'{wrong_callable} must be a callable that accepts'
                   ' (i) a value, (ii) an optional name for that value,'
                   ' and (iii) any number of keyword arguments!')
        with self.assertRaises(CallableError) as err:
            _ = CompositionOf(self.f, wrong_callable)
        self.assertEqual(str(err.exception), err_msg)


class TestCompositionOf(ut.TestCase):

    def setUp(self):
        self.f = lambda x, name=None: x**2
        self.g = lambda y, name=None: y - 3
        self.h = lambda z, name=None: 4*z
        self.u = lambda x, name=None: (3*x - 1)/7
        self.wrong_signature = lambda y: y
        self.comp = CompositionOf(self.f, self.g)

    def test_is_callable(self):
        self.assertTrue(callable(self.comp))

    def test_error_on_first_callable_wrong_signature(self):
        comp = CompositionOf(self.wrong_signature, self.g)
        err_msg = ('<lambda> must be a callable that accepts (i) '
                   'a value, (ii) an optional name for that value,'
                   ' and (iii) any number of keyword arguments!')
        with self.assertRaises(CallableError) as err:
            _ = comp(1)
        self.assertEqual(str(err.exception), err_msg)

    def test_error_on_second_callable_wrong_signature(self):
        comp = CompositionOf(self.f, self.wrong_signature)
        err_msg = ('<lambda> must be a callable that accepts (i) '
                   'a value, (ii) an optional name for that value,'
                   ' and (iii) any number of keyword arguments!')
        with self.assertRaises(CallableError) as err:
            _ = comp(1)
        self.assertEqual(str(err.exception), err_msg)

    def test_associativity_of_composition(self):
        comp1 = CompositionOf(CompositionOf(self.f, self.g), self.h)
        comp2 = CompositionOf(self.f, CompositionOf(self.g, self.h))
        self.assertTrue(all(comp1(x) == comp2(x) for x in range(-100, 100)))

    def test_has_attribute_o(self):
        self.assertTrue(hasattr(self.comp, 'o'))

    def test_attribute_o_is_callable(self):
        self.assertTrue(callable(self.comp.o))

    def test_o_returns_composition(self):
        return_value = self.comp.o(self.h)
        self.assertIsInstance(return_value, CompositionOf)

    def test_o_raises_error_on_argument_not_callable(self):
        comp = self.comp.o(self.h)
        class WrongCallable:
            __name__ = 'Named object'
        wrong_callable = WrongCallable()
        err_msg = ('Named object must be a callable that accepts (i)'
                   ' a value, (ii) an optional name for that value,'
                   ' and (iii) any number of keyword arguments!')
        with self.assertRaises(CallableError) as err:
            _ = comp.o(wrong_callable)
        self.assertEqual(str(err.exception), err_msg)

    def test_o_is_equivalent_to_explicit_composition(self):
        comp1 = CompositionOf(self.comp, self.h)
        comp2 = self.comp.o(self.h)
        self.assertTrue(all(comp1(x) == comp2(x) for x in range(-100, 100)))

    def test_copies_lowercase_attributes_of_second_callable(self):
        self.h.foo = 'foo'
        comp2 = self.comp.o(self.h)
        self.assertTrue(hasattr(comp2, 'foo'))
        self.assertEqual(comp2.foo, 'foo')

    def test_ignores_non_callable_uppercase_attributes(self):
        self.h.Bar = 'bar'
        comp2 = self.comp.o(self.h)
        self.assertFalse(hasattr(comp2, 'Bar'))

    def test_copies_composition_of_uppercase_callable_attributes(self):
        self.h.Baz = self.u
        comp2 = self.comp.o(self.h)
        self.assertTrue(hasattr(comp2, 'Baz'))
        self.assertIsInstance(comp2.Baz, CompositionOf)

    def test_copied_equivalent_to_direct_composition(self):
        direct = self.comp.o(self.h).o(self.u)
        self.h.U = self.u
        copied = self.comp.o(self.h)
        self.assertTrue(all(direct(x) == copied.U(x) for x in range(-99, 100)))

    def test_has_attribute_name(self):
        comp = CompositionOf(self.f, self.g)
        self.assertTrue(hasattr(comp, '__name__'))

    def test_copies_name_of_second_callable(self):
        self.g.__name__ = 'second'
        comp = CompositionOf(self.f, self.g)
        self.assertEqual(comp.__name__, 'second')

    def test_has_docstring(self):
        comp = CompositionOf(self.f, self.g)
        self.assertTrue(hasattr(comp, '__doc__'))

    def test_copied_docstring_from_second_callable(self):
        self.g.__doc__ = 'docstring'
        comp = CompositionOf(self.f, self.g)
        self.assertEqual(comp.__doc__, 'docstring')


if __name__ == '__main__':
    ut.main()
