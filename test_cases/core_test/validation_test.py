import unittest
from core.validation import helpers


class ValidationTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_phone_number_is_empty(self):
        result = helpers.is_not_empty_phone_number("")
        self.assertEqual(result, False)

    def test_phone_number_is_not_empty(self):
        result = helpers.is_not_empty_phone_number("09372943761")
        self.assertEqual(result, True)

    def test_password_is_strength(self):

        self.assertEqual(helpers.password_regex_checker("ABC321$eeee"), (True,))
        self.assertEqual(helpers.password_regex_checker("Amish123456"), (True,))

    def test_password_is_not_strength(self):
        self.assertEqual(helpers.password_regex_checker("123456789"), (False, 'password_is_not_strength'))
        self.assertEqual(helpers.password_regex_checker("1111111111"), (False, 'password_is_not_strength'))
        self.assertEqual(helpers.password_regex_checker(""), (False, 'password_is_not_strength'))

    def test_mobile_regex(self):
        pass


    # runs the unit tests in the module


if __name__ == '__main__':
    unittest.main()
