import unittest
import day_02 as day

test_data = day.read_text_file("02_test.txt")

class TestMethods(unittest.TestCase):

    def test_1(self):

        score = day.part_1(test_data)

        self.assertEqual(score, 8)


    def test_2(self):

        score = day.part_2(test_data)

        self.assertEqual(score, 2286)


if __name__ == '__main__':
    unittest.main()

