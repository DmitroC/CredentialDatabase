import unittest
from CredentialDatabase.utils.password import Password


class TestPassword(unittest.TestCase):

    def setUp(self) -> None:

        # set up a password instance
        self.password = Password()

    def test_is_symbol(self):

        self.assertTrue(self.password.is_symbol(password='abc+33'), msg="test is_symbol failed")
        self.assertFalse(self.password.is_symbol(password='test123'), msg="test is_symbol failed")

    def test_is_number(self):

        self.assertTrue(self.password.is_number(password='test123'), msg="test is_number failed")
        self.assertFalse(self.password.is_number(password='test'), msg="test is_number failed")

    def test_generate_hashes(self):

        sha1, sha256, sha512, md5 = self.password.generate_hashes(password='test1234')

        self.assertEqual(sha1, '9bc34549d565d9505b287de0cd20ac77be1d3f2c', msg="hash function sha1 failed")
        self.assertEqual(sha256, '937e8d5fbb48bd4949536cd65b8d35c426b80d2f830c5c308e2cdec422ae2244', msg="hash function sha256 failed")
        self.assertEqual(sha512, '2bbe0c48b91a7d1b8a6753a8b9cbe1db16b84379f3f91fe115621284df7a48f1cd71e9beb90ea614c7bd924250aa9e446a866725e685a65df5d139a5cd180dc9', msg="hash function sha512 failed")
        self.assertEqual(md5, '16d7a4fca7442dda3ad93c9a726597e4', msg="hash function md5 failed")

    def tearDown(self) -> None:
        pass


if __name__ == '__main__':
    unittest.main()
