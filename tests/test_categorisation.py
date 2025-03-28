import unittest
from src.main import categorise_transactions

class TestCategorisation(unittest.TestCase):
    def test_01(self):
        self.assertEqual(categorise_transactions(account = "Marketing", department = "Traffic"), "Traffic")
    def test_02(self):
        self.assertEqual(categorise_transactions(account = "Marketing", department = "IT"), "Marketing")
    def test_03(self):
        self.assertEqual(categorise_transactions(account = "Marketing", department = ""), "Marketing")
    def test_04(self):
        self.assertEqual(categorise_transactions(account = "Finance", department = "Traffic"), "Other")
    def test_05(self):
        self.assertEqual(categorise_transactions(account = "", department = "Traffic"), "Other")
    def test_06(self):
        self.assertEqual(categorise_transactions(account = "", department = "IT"), "Other")
    def test_07(self):
        self.assertEqual(categorise_transactions(account = "", department = ""), "Other")
    def test_08(self):
        self.assertEqual(categorise_transactions(account = "Finance", department = "Traffic"), "Other")