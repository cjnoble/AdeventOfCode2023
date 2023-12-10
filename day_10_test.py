import unittest
import day_10 as day

DAY = "10"
test_data_1 = day.read_text_file(f"{DAY}_test_1.txt")
test_data_2 = day.read_text_file(f"{DAY}_test_2.txt")

test_data_2_1 = day.read_text_file(f"{DAY}_test_3.txt")
test_data_2_2 = day.read_text_file(f"{DAY}_test_4.txt")
test_data_2_3 = day.read_text_file(f"{DAY}_test_5.txt")

class TestMethods(unittest.TestCase):

    def test_part_1_1(self):

        self.assertEqual(day.part_1(test_data_1)[0], 4)

    def test_part_1_2(self):

        self.assertEqual(day.part_1(test_data_2)[0], 8)

    def test_part_2_1(self):

        self.assertEqual(day.part_2(test_data_2_1), 4)

    def test_part_2_2(self):

        self.assertEqual(day.part_2(test_data_2_2), 8)

    def test_part_2_3(self):

        self.assertEqual(day.part_2(test_data_2_3), 10)


if __name__ == '__main__':
    unittest.main()