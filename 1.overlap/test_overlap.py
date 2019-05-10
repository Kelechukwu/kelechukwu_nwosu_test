import unittest
from overlap import overlap

class TestOverlap(unittest.TestCase):
    def setUp(self):
        # load test inputs
        self.non_overlaping_lines = [
            [(1,5),(6,8)],
            [(1,4),(4,12)],
            [(2,12),(9,12)],
        ]
        self.overlaping_lines = [
            [(1,5),(2,6)],
            [(2,6),(1,5)],
            [(2,4),(3,12)],
        ]


    def test_overlapping_lines(self):
        for lines in self.overlaping_lines:
            result = overlap(lines[0],lines[1])
            self.assertTrue(result)


    def test_non_overlapping_lines(self):
        for lines in self.non_overlaping_lines:
            result = overlap(lines[0],lines[1])
            self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()