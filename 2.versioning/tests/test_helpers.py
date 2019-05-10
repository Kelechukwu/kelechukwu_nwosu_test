import os
import sys
import unittest

# Add grandparent directory to sys.path 
# this is so that helpers module can be imported
# when running tests directly 
sys.path.append(os.path.abspath(__file__ + "/../../"))

from version.helpers import tokenize_version_string, add_filler

class TestHelperFunctions(unittest.TestCase):
    
    def test_tokenize_version_string(self):
        return_value = tokenize_version_string("1.2")
        expectation = ["1", "2"]
        self.assertEqual(return_value, expectation)

        return_value = tokenize_version_string("2.2.1")
        expectation = ["2", "2", "1"]
        self.assertEqual(return_value, expectation)

        return_value = tokenize_version_string("1.2b")
        expectation = ["1", "2", "b"]
        self.assertEqual(return_value, expectation)

        return_value = tokenize_version_string("1.2bc")
        expectation = ["1", "2", "b","c"]
        self.assertEqual(return_value, expectation)

        return_value = tokenize_version_string("1.2.a")
        expectation = ["1", "2", "a"]
        self.assertEqual(return_value, expectation)

        return_value = tokenize_version_string("NT 1.1")
        expectation = ["1", "1"]
        self.assertEqual(return_value, expectation)
    
    def test_add_filler(self):
        return_value = add_filler(["1", "2"], ["1", "2", "3"])
        expectation = (["1", "2", "0"], ["1", "2", "3"])
        self.assertEqual(return_value, expectation)

        return_value = add_filler(["1", "2", "a"], ["1", "2", "a"])
        expectation = (["1", "2", "a"], ["1", "2", "a"])
        self.assertEqual(return_value, expectation)


if __name__ == '__main__':
    unittest.main()