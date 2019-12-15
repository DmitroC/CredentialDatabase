import unittest
from CredentialDatabase.utils.password import Password


class TestPassword(unittest.TestCase):

    def setUp(self) -> None:

        # set up a password instancde
        self.password = Password()

    def test_is_symbol(self):
        pass

    def test_is_number(self):
        pass

    def test_generate_hashes(self):
        pass

    def tearDown(self) -> None:
        pass


if __name__ == '__main__':
    unittest.main()
