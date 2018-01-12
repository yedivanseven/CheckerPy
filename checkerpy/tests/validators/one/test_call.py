import logging
import unittest as ut
from ....validators.one import Call
from ....exceptions import CallableError


class TestCall(ut.TestCase):

    def test_works_with_sane_callable(self):
        inp = lambda x: x
        out = Call(inp)
        self.assertIs(out, inp)

    def test_error_on_unnamed_object_without_name_attr(self):
        log_msg = ['ERROR:root:Object foo of type str is not callable!']
        err_msg = 'Object foo of type str is not callable!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(CallableError) as err:
                _ = Call('foo')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_object_without_name_attr(self):
        log_msg = ['ERROR:root:Object test of type int is not callable!']
        err_msg = 'Object test of type int is not callable!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(CallableError) as err:
                _ = Call(1, 'test')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_unnamed_object_with_name_attr(self):
        class Test:
            pass
        t = Test()
        t.__name__= 'test'
        log_msg = ['ERROR:root:Object test of type Test is not callable!']
        err_msg = 'Object test of type Test is not callable!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(CallableError) as err:
                _ = Call(t)
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)

    def test_error_on_named_object_with_name_attr(self):
        class Test:
            pass
        t = Test()
        t.__name__= 'test'
        log_msg = ['ERROR:root:Object name of type Test is not callable!']
        err_msg = 'Object name of type Test is not callable!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(CallableError) as err:
                _ = Call(t, 'name')
        self.assertEqual(str(err.exception), err_msg)
        self.assertEqual(log.output, log_msg)


if __name__ == '__main__':
    ut.main()
