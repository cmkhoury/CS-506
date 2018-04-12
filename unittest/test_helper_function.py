import unittest
import sys
sys.path.append("..")
import helper_function

class test_helper_function(unittest.TestCase):
    def setUp(self):
        pass

    def testCalculateCost(self):
        self.assertEqual(helper_function.CalculateCost(13.6, 4.7), 18.3)

    def testCalculateLeft(self):
        self.assertEqual(round(helper_function.CalculateLeft(13.6, 4.7),1), 8.9)

    def testReachLineTrue(self):
        self.assertFalse(helper_function.ReachLine(1, 3))

    def testReachLineFalse(self):
        self.assertFalse(helper_function.ReachLine(3, 1))

    def testCheckPasswordTrue(self):
        passwordInput = 'aaa'
        passwordHashed = '$2b$12$uU/1jW9wz0n7iYAluZP7LuvF/.7/BnEwkn40TL3lJAD1uHmOKQn6S'
        self.assertTrue(helper_function.checkPassword(passwordInput.encode(), passwordHashed.encode()))

if __name__=='__main__':
    unittest.main()
