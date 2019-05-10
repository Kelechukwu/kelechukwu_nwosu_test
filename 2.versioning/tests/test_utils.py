import os
import sys
import unittest

# Add grandparent directory to sys.path 
# this is so that version module can be imported
# when running tests directly 
sys.path.append(os.path.abspath(__file__ + "/../../"))

from version.utils import compare

class TestVersionComparison(unittest.TestCase):
    def setUp(self):
        # load test examples

        self.greater_than = [
            ("1.2", "1.1"), # greater
            ("2.2.1", "2.1.1"), # greater from second digit
            ("2.2.3", "2.2.1"), # greater at the final digit
            ("1.2", "1.1.3"), # greater (combination of 2 and 3 digit version strings)
            ("1.2b", "1.2a"), # greater ( alphanumeric version strings)
            ("1.2.b", "1.2.a"), # greater ( alphanumeric version strings all seperated by dots)
        ]

        self.less_than = [
            ("0.1", "0.5"), # less
            ("0.1.1", "0.1.5"), # less at final digit
            ("0.1.1", "0.2.1"), # less at second digit
            ("0.1", "0.5.1"), # less (combination of 2 and 3 digit version strings)
            ("0.1a", "0.1b"), # less ( alphanumeric version strings)
            ("0.1.a", "0.1.b"), # less ( alphanumeric version strings all seperated by dots)
        ]

        self.equal = [
            ("3.1", "3.1"), # equal
            ("3.8.1", "3.8.1"), # equal
            ("0.1a", "0.1a"), # equal( alphanumeric)
            ("0.1.a", "0.1.a"), # equal ( alphanumeric version strings all seperated by dots)
            ("NT 1.1", "NT 1.1"), # equal ( with prefix)
        ]

    
    def test_greater_than(self):
        for versions_tuple in self.greater_than:
            returned_string = compare(versions_tuple[0], versions_tuple[1])
            expectation = f"{versions_tuple[0]} > {versions_tuple[1]}"
            self.assertEqual(returned_string,expectation)


    def test_less_than(self):
        for versions_tuple in self.less_than:
            returned_string = compare(versions_tuple[0], versions_tuple[1])
            expectation = f"{versions_tuple[0]} < {versions_tuple[1]}"
            self.assertEqual(returned_string,expectation)


    def test_equal_to(self):
        for versions_tuple in self.equal:
            returned_string = compare(versions_tuple[0], versions_tuple[1])
            expectation = f"{versions_tuple[0]} == {versions_tuple[1]}"
            self.assertEqual(returned_string,expectation)


if __name__ == '__main__':
    unittest.main()