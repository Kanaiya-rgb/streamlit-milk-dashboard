import pytest
import pandas as pd
from src.data.load_data import load_data

def test_load_data():
    df = load_data()
    
    # Check if the DataFrame is not empty
    assert not df.empty, "DataFrame is empty"
    
    # Check if the expected columns are present
    expected_columns = ['Date of Record', 'Month', 'How much milk received? (ml/Liters)', 'Milk Received?']
    for column in expected_columns:
        assert column in df.columns, f"Missing column: {column}"
    
    # Check if the 'How much milk received? (ml/Liters)' column is of integer type after conversion
    assert pd.api.types.is_integer_dtype(df['How much milk received? (ml/Liters)']), "Column type is not integer"
    
    # Check if 'Date of Record' is in datetime format
    assert pd.api.types.is_datetime64_any_dtype(df['Date of Record']), "Date of Record is not in datetime format"