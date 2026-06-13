# app/dataset/tests.py

import unittest
import os
from app.dataset.validators import validate_csv


class DatasetTest(unittest.TestCase):

    def setUp(self):
        # create a temporary csv file for testing
        self.test_file = "test_dataset.csv"
        with open(self.test_file, "w") as f:
            f.write("name,age\nJohn,20\nJane,25")

    def tearDown(self):
        # remove test file after each test
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_valid_csv(self):
        result = validate_csv(self.test_file)
        self.assertTrue(result)

    def test_invalid_file(self):
        with self.assertRaises(ValueError):
            validate_csv("data.txt")

    def test_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            validate_csv("missing.csv")


if __name__ == "__main__":
    unittest.main()