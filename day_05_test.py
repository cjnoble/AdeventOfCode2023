import unittest
import day_05 as day

DAY = "05"
test_data = day.read_text_file(f"{DAY}_test.txt")

class TestMethods(unittest.TestCase):

    def test_1(self):

        expected = 35

        result = day.part_1(test_data)

        self.assertEqual(result, expected)

    def test_2(self):

        expected = 46

        result = day.part_2(test_data)

        self.assertEqual(result, expected)


    def test_2_bf(self):

        expected = 46

        result = day.part_2_bruteforce(test_data)

        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()