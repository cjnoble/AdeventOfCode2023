import unittest
import day_17 as day

DAY = "17"
test_data = day.read_text_file(f"{DAY}_test.txt")

class TestMethods(unittest.TestCase):

    def test_small(self):

        expected = 10

        result = day.part_1([[1, 1, 1, 2, 1],
                             [1, 2, 2, 1, 1],
                             [1, 2, 5, 1, 1],
                             [2, 1, 1, 2, 1],
                             [1, 1, 1, 1, 1],
                             [1, 1, 1, 1, 1]])

        self.assertEqual(result, expected)

    def test_small_2(self):

        expected = 31

        result = day.part_1([[1, 1, 1, 2, 1, 1, 22, 1, 1, 1, 1, 1, 1],
                             [1, 1, 1, 2, 1, 1, 22, 1, 1, 1, 1, 1, 1],
                             [1, 1, 1, 2, 1, 1, 22, 1, 1, 1, 1, 1, 1],
                             [1, 1, 1, 2, 1, 1, 22, 1, 1, 1, 1, 1, 1],
                             [1, 1, 1, 2, 1, 1, 22, 1, 22, 1, 1, 1, 1],
                             [1, 1, 1, 2, 1, 1, 22, 1, 22, 1, 1, 1, 1],
                             [1, 1, 1, 2, 1, 1, 1, 1, 22, 1, 1, 1, 1],
                             [1, 1, 1, 2, 1, 1, 1, 1, 22, 1, 1, 1, 1],
                             [1, 1, 1, 2, 1, 1, 1, 1, 22, 1, 1, 1, 1],
                             [1, 1, 1, 2, 1, 1, 1, 1, 22, 1, 1, 1, 1],
                             [1, 1, 1, 2, 1, 1, 1, 1, 22, 1, 1, 1, 1],
                             [1, 1, 1, 2, 1, 1, 1, 1, 22, 1, 1, 1, 1],
                             [1, 1, 1, 2, 1, 1, 1, 1, 22, 1, 1, 1, 1],
                             ])

        self.assertEqual(result, expected)

    def test_1(self):

        expected = 102

        result = day.part_1(test_data)

        self.assertEqual(result, expected)

    def test_2(self):

        expected = 94

        result = day.part_2(test_data)

        self.assertEqual(result, expected)

    def test_2_2(self):

        expected = 71

        result = day.part_2([
            [1,1,1,1,1,1,1,1,1,1,1,1],
            [9,9,9,9,9,9,9,9,9,9,9,1],
            [9,9,9,9,9,9,9,9,9,9,9,1],
            [9,9,9,9,9,9,9,9,9,9,9,1],
            [9,9,9,9,9,9,9,9,9,9,9,1]])

        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()