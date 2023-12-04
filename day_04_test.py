import unittest
import day_04 as day

DAY = "04"
test_data = day.read_text_file(f"{DAY}_test.txt")

class TestMethods(unittest.TestCase):

    def test_1(self):

        expected = 13

        result = day.part_1(test_data)

        self.assertEqual(result, expected)

    def test_2(self):

        expected = 30

        result = day.part_2(test_data)

        self.assertEqual(result, expected)

    def test_n_wins(self):

        result = day.n_wins([1, 2, 3], [2, 3, 4])
        self.assertEqual(result, 2)

if __name__ == '__main__':
    unittest.main()