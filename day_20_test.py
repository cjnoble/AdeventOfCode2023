import unittest
import day_20 as day

DAY = "20"
test_data = day.read_text_file(f"{DAY}_test.txt")

class TestMethods(unittest.TestCase):


    def test_1_simple(self):

        expected = 32000000

        result = day.part_1([r"broadcaster -> a, b, c", r"%a -> b", r"%b -> c", r"%c -> inv", r"&inv -> a"], 1000)

        self.assertEqual(result, expected)

    def test_1(self):

        expected = 11687500

        result = day.part_1(test_data, 1000)

        self.assertEqual(result, expected)

    def test_2(self):

        expected = 0

        result = day.part_2(test_data)

        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()