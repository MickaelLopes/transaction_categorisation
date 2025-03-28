import unittest
import pandas as pd
from src.main import categorise_transaction, transactions_categorisation

class TestCategorisation(unittest.TestCase):
    def test_01(self):
        self.assertEqual(categorise_transaction(account = "Marketing", department = "Traffic"), "Traffic")
    def test_02(self):
        self.assertEqual(categorise_transaction(account = "Marketing", department = "IT"), "Marketing")
    def test_03(self):
        self.assertEqual(categorise_transaction(account = "Marketing", department = ""), "Marketing")
    def test_04(self):
        self.assertEqual(categorise_transaction(account = "Finance", department = "Traffic"), "Other")
    def test_05(self):
        self.assertEqual(categorise_transaction(account = "", department = "Traffic"), "Other")
    def test_06(self):
        self.assertEqual(categorise_transaction(account = "", department = "IT"), "Other")
    def test_07(self):
        self.assertEqual(categorise_transaction(account = "", department = ""), "Other")
    def test_08(self):
        self.assertEqual(categorise_transaction(account = "Finance", department = "Traffic"), "Other")
        
class TestTransactionCategorisation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.df = pd.DataFrame([
            {"Date": "1-Jan-25", "Debit": 0.00, "Credit": 93.21, "Account": "Marketing", "Department": "Traffic"},
            {"Date": "25-Feb-25", "Debit": 1324.00, "Credit": 0.00, "Account": "Finance", "Department": "Rent"},
            {"Date": "23-Feb-25", "Debit": 15.00, "Credit": 1.00, "Account": "Marketing", "Department": None},
            {"Date": "22-Feb-25", "Debit": 25134.45, "Credit": 0.00, "Account": "IT", "Department": "Infra"},
        ])
        cls.result = transactions_categorisation(cls.df)
        
    def test_jan_traffic(self):
        month_filter = self.result["Month"] == "January"
        category_filter = self.result["Category"] == "Traffic"
        self.assertEqual(self.result.loc[month_filter & category_filter, "Total"].values[0], -93.21)
    
    def test_jan_marketing(self):
        month_filter = self.result["Month"] == "January"
        category_filter = self.result["Category"] == "Marketing"
        self.assertEqual(self.result.loc[month_filter & category_filter, "Total"].values[0], 0.0)
        
    def test_jan_other(self):
        month_filter = self.result["Month"] == "January"
        category_filter = self.result["Category"] == "Other"
        self.assertEqual(self.result.loc[month_filter & category_filter, "Total"].values[0], 0.0)
        
    def test_feb_traffic(self):
        month_filter = self.result["Month"] == "February"
        category_filter = self.result["Category"] == "Traffic"
        self.assertEqual(self.result.loc[month_filter & category_filter, "Total"].values[0], 0.0)
    
    def test_feb_marketing(self):
        month_filter = self.result["Month"] == "February"
        category_filter = self.result["Category"] == "Marketing"
        self.assertEqual(self.result.loc[month_filter & category_filter, "Total"].values[0], 14.0)
        
    def test_feb_other(self):
        month_filter = self.result["Month"] == "February"
        category_filter = self.result["Category"] == "Other"
        self.assertEqual(self.result.loc[month_filter & category_filter, "Total"].values[0], 26458.45)