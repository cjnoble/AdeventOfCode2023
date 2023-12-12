import unittest
import day_12 as day

DAY = "12"
test_data = day.read_text_file(f"{DAY}_test.txt")

class TestMethods(unittest.TestCase):

    def test_1(self):

        expected = 21

        result = day.part_1(test_data)

        self.assertEqual(result, expected)

    def test_1_p1p2_compare(self):

        real_data =  day.read_text_file(f"{DAY}.txt")
        result = day.part_1_compare(real_data)

        self.assertTrue(True)


    def test_1_p1p2(self):

        expected = 7916
        real_data =  day.read_text_file(f"{DAY}.txt")
        result = day.part_1_optimum(real_data)

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


    def test_4(self):
        expected = 16

        result = day.part_2_nonconcurrent(["????.#...#... 4,1,1"])

        self.assertEqual(result, expected)

    def test_custom(self):
        expected = 1

        result = day.part_2_nonconcurrent(["?#?#?#?#?#?#?#? 1,3,1,6"])

        self.assertEqual(result, expected)

    def test_custom_1(self):
        expected = 15

        result = day.part_1_optimum(["??##??????????.?# 4,4,2"])

        self.assertEqual(result, expected)

#'??##??????????.?# 4,4,2'

if __name__ == '__main__':
    unittest.main()