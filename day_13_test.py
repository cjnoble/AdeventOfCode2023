import unittest
import day_13 as day

DAY = "13"
test_data = day.read_text_file(f"{DAY}_test.txt")
test_data2 = day.read_text_file(f"{DAY}_test2.txt")

class TestMethods(unittest.TestCase):

    def test_1(self):

        expected = 405

        result = day.part_1(test_data)

        self.assertEqual(result, expected)


    def test_2(self):

        expected = 400

        result = day.part_2(test_data)

        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()