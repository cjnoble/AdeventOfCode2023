import unittest
import day_01


test_data = day_01.read_text_file("01_test.txt")
test_data_2 = day_01.read_text_file("01_2_test.txt")

class TestMethods(unittest.TestCase):

    def test_1(self):

        score = day_01.part_1(test_data)

        self.assertEqual(score, 142)


    def test_2(self):

        score = day_01.part_2(test_data_2)

        self.assertEqual(score, 281)

    def test_3(self):

        score = day_01.part_2(["oneeight5"])

        self.assertEqual(score, 15)
    
    def test_4(self):

        score = day_01.part_2(["oneight"])

        self.assertEqual(score, 18)

if __name__ == '__main__':
    unittest.main()

