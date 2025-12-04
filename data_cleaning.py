import pandas as pd
import numpy as np
from pathlib import Path

csv_file_path = Path('C:/Users/silly/Downloads/sales_data_raw.csv')
data = pd.read_csv(csv_file_path)

# This function puts all column titles as lowercase (thanks copilot!)
def column_standardization_lowercase(df: pd.DataFrame) -> pd.DataFrame:
	"""Standardize column names by converting them to lowercase.
	
	This function takes a DataFrame and returns a new DataFrame with all
	column names converted to lowercase for consistency.
	"""
	df = df.copy()
	df.columns = df.columns.str.lower()
	return df


data = column_standardization_lowercase(data)

# This function removes the whitespaces from product name and categories 
def Whitespace_removal(df: pd.DataFrame) -> pd.DataFrame:
	"""Strip leading and trailing whitespace from prodname and category columns.
	
	This function removes leading and trailing whitespace, and collapses internal
	whitespace to single spaces from the 'prodname' and 'category' columns.
	"""
	df = df.copy()
	if 'prodname' in df.columns:
		df['prodname'] = df['prodname'].str.strip()
		df['prodname'] = df['prodname'].apply(lambda x: ' '.join(str(x).split()))
	if 'category' in df.columns:
		# Strip whitespace and collapse internal whitespace, keep quotes
		df['category'] = df['category'].str.strip()
		df['category'] = df['category'].apply(lambda x: ' '.join(str(x).split()))
	return df


data = Whitespace_removal(data)
print(data)