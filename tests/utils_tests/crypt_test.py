from unittest import TestCase

from utils.crypt import gen_salt


class TestCrypt(TestCase):
    def gen_salt(self):
        LEN = 5
        salt = gen_salt(LEN)
        self.assertEqual(len(salt), LEN)

    def gen_salt_less(self):
        LEN = 0
        with self.assertRaises(ValueError):
            gen_salt(LEN)

    def gen_salt_more(self):
        LEN = 50
        salt = gen_salt(LEN)
        self.assertEqual(len(salt, LEN))
