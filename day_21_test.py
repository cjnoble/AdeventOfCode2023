import unittest
import day_21 as day

DAY = "21"
test_data = day.read_text_file(f"{DAY}_test.txt")

class TestMethods(unittest.TestCase):

    def test_1(self):

        expected = 16

        result = day.part_1(test_data, 6)

        self.assertEqual(result, expected)

    def test_p1_1(self):

        steps = 0
        expected = 1

        result = day.part_1(test_data, steps)

        self.assertEqual(result, expected)

    def test_p1_2(self):

        steps = 1
        expected = 2

        result = day.part_1(test_data, steps)

        self.assertEqual(result, expected)

    def test_p1_3(self):

        steps = 2
        expected = 4

        result = day.part_1(test_data, steps)

        self.assertEqual(result, expected)

    def test_p2_1(self):

        steps = 6
        expected = 16

        result = day.part_2(test_data, steps)

        self.assertEqual(result, expected)

    def test_p2_2(self):

        steps = 10
        expected = 50

        result = day.part_2(test_data, steps)

        self.assertEqual(result, expected)

    def test_p2_3(self):

        steps = 50
        expected = 1594

        result = day.part_2(test_data, steps)

        self.assertEqual(result, expected)


    def test_p2_4(self):

        steps = 100
        expected = 6536

        result = day.part_2(test_data, steps)

        self.assertEqual(result, expected)

    def test_p2_5(self):

        steps = 500
        expected = 167004

        result = day.part_2(test_data, steps)

        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()