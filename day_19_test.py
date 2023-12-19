import unittest
import day_19 as day

DAY = "19"
test_data = day.read_text_file(f"{DAY}_test.txt")

class TestMethods(unittest.TestCase):

    def test_1(self):

        expected = 19114

        result = day.part_1(test_data)

        self.assertEqual(result, expected)

    def test_2(self):
                    #64059931636842
        expected = 167409079868000

        result = day.part_2(test_data)

        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()