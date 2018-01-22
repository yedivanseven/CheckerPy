import unittest as ut
from ...decorators.typeparser import TypeParser


class TestBoundsParser(ut.TestCase):

    def setUp(self):
        self.parse = TypeParser()

    def test_error_on_argument_not_tuple_or_dict(self):
        err_msg = ('Iterator with specifications for argument checkers must'
                   ' be a tuple (if specified in *args format) or a dict '
                   '(if specified in **kwargs format), not str like foo!')
        with self.assertRaises(TypeError) as err:
            _ = self.parse('foo')
        self.assertEqual(str(err.exception), err_msg)


if __name__ == '__main__':
    ut.main()
