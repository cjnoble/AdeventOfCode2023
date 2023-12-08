import unittest
import day_08 as day

DAY = "08"
test_data_1 = day.read_text_file(f"{DAY}_test_01.txt")
test_data_2 = day.read_text_file(f"{DAY}_test_02.txt")
test_data_3 = day.read_text_file(f"{DAY}_test_03.txt")

class TestMethods(unittest.TestCase):

    def test_1(self):

        self.assertEqual(day.part_1(test_data_1), 2)
        self.assertEqual(day.part_1(test_data_2), 6)

    def test_2(self):

        self.assertEqual(day.part_2(test_data_3), 6)


if __name__ == '__main__':
    unittest.main()