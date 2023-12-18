import unittest
import day_18 as day

DAY = "18"
test_data = day.read_text_file(f"{DAY}_test.txt")

class TestMethods(unittest.TestCase):

    def test_1(self):

        expected = 62
        expected_perimeter = 38

        result = day.part_1(test_data)

        self.assertEqual(result, expected)

    def test_2(self):

        expected = 952408144115

        result = day.part_2(test_data)

        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()