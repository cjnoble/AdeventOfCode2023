import unittest
import day_12 as day

DAY = "12"
test_data = day.read_text_file(f"{DAY}_test.txt")

class TestMethods(unittest.TestCase):

    def test_1(self):

        expected = 21

        result = day.part_1(test_data)

        self.assertEqual(result, expected)

    def test_2_nc(self):

        expected = 525152

        result = day.part_2_nonconcurrent(test_data)

        self.assertEqual(result, expected)

    def test_2(self):

        expected = 525152

        result = day.part_2(test_data)

        self.assertEqual(result, expected)

    def test_slow_case(self):
        expected = 506250

        result = day.part_2_nonconcurrent(["?###???????? 3,2,1"])

        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()