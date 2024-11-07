import unittest
from unittest.mock import patch
import pandas as pd
import numpy as np

# Import functions from gdp_extractor
from gdp_extractor import fetch_data, process_data

class TestGDPFunctions(unittest.TestCase):
    
    @patch('pandas.read_html')
    def test_fetch_data(self, mock_read_html):
        """Test that fetch_data extracts the correct table from the URL."""
        print("\nTesting fetch_data function...")
        
        # Mock HTML tables returned by pandas.read_html
        mock_tables = [
            pd.DataFrame({"A": [1, 2], "B": [3, 4]}),  # Table 0
            pd.DataFrame({"A": [5, 6], "B": [7, 8]}),  # Table 1
            pd.DataFrame({"A": [9, 10], "B": [11, 12]}),  # Table 2
            pd.DataFrame({0: ["Country A", "Country B", "Country C"], 
                          1: [1000, 2000, 3000], 
                          2: [1000000, 2000000, 3000000]})  # Table 3
        ]
        mock_read_html.return_value = mock_tables
        
        # URL is not used here as read_html is mocked
        url = "https://example.com/imf-gdp-data"
        data = fetch_data(url)
        
        # Check that the third table (index 3) was selected
        print("Asserting the first country in the table is 'Country A'...")
        self.assertEqual(data.iloc[0, 0], "Country A", "Expected 'Country A' as the first country.")
        
        print("Asserting the GDP for 'Country A' is 1000000...")
        self.assertEqual(data.iloc[0, 2], 1000000, "Expected GDP of 1000000 for 'Country A'.")

    def test_process_data(self):
        """Test that process_data correctly processes data by selecting specific columns and rows, converting GDP to billions, and renaming columns."""
        print("\nTesting process_data function...")
        
        # Create a DataFrame to mock input data
        data = pd.DataFrame({
            0: ["Header", "Country A", "Country B", "Country C", "Country D", 
                "Country E", "Country F", "Country G", "Country H", "Country I", "Country J"],
            1: [None, 1000, 900, 800, 700, 600, 500, 400, 300, 200, 100],
            2: [None, 1000000, 900000, 800000, 700000, 600000, 500000, 400000, 300000, 200000, 100000]
        })
        
        # Process the data
        top_10 = process_data(data)
        
        # Check that top_10 DataFrame has correct shape and headers
        print("Asserting shape of processed DataFrame is (10, 2)...")
        self.assertEqual(top_10.shape, (10, 2), "Expected 10 rows and 2 columns in processed DataFrame.")
        
        print("Asserting column headers are ['Country', 'GDP (Billion USD)']...")
        self.assertListEqual(list(top_10.columns), ["Country", "GDP (Billion USD)"], "Expected columns to be ['Country', 'GDP (Billion USD)'].")
        
        # Validate content: first and last rows with GDP values converted to billions
        print("Asserting first row's country is 'Country A' and GDP is 1000.00 billion USD...")
        self.assertEqual(top_10.iloc[0]["Country"], "Country A", "Expected 'Country A' as the first country.")
        self.assertAlmostEqual(top_10.iloc[0]["GDP (Billion USD)"], 1000.00, places=2, msg="Expected GDP of 1000.00 billion USD for 'Country A'.")
        
        print("Asserting last row's country is 'Country J' and GDP is 100.00 billion USD...")
        self.assertEqual(top_10.iloc[-1]["Country"], "Country J", "Expected 'Country J' as the last country.")
        self.assertAlmostEqual(top_10.iloc[-1]["GDP (Billion USD)"], 100.00, places=2, msg="Expected GDP of 100.00 billion USD for 'Country J'.")

if __name__ == "__main__":
    unittest.main()
