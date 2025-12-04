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

# Strip whitespace from column names
data.columns = data.columns.str.strip()

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


def row_removal(df: pd.DataFrame) -> pd.DataFrame:
	"""Remove rows with negative prices or negative quantities.
	
	This function filters out any rows where the 'price' column contains
	a negative value or the 'qty' column contains a negative value.
	"""
	df = df.copy()
	
	# Find price and qty columns (case-insensitive, ignoring spaces)
	price_col = None
	qty_col = None
	
	for col in df.columns:
		col_lower = col.lower().strip()
		if col_lower == 'price':
			price_col = col
		elif col_lower == 'qty':
			qty_col = col
	
	# Remove rows with negative prices
	if price_col:
		df[price_col] = pd.to_numeric(df[price_col], errors='coerce')
		df = df[df[price_col] >= 0]
	
	# Remove rows with negative quantities
	if qty_col:
		df[qty_col] = pd.to_numeric(df[qty_col], errors='coerce')
		df = df[df[qty_col] >= 0]
	
	return df


data = row_removal(data)


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
	"""Handle missing values in price, quantity, and date_sold columns.
	
	- Missing values in 'price' column are filled with "Missing"
	- Missing values in 'qty' column are filled with "0"
	- Missing values in 'date_sold' column are filled with "Missing"
	"""
	df = df.copy()
	
	# Find columns (case-insensitive, ignoring spaces)
	for col in df.columns:
		col_lower = col.lower().strip()
		if col_lower == 'price':
			# fillna on both numeric NaN and string 'NaN'
			df[col] = df[col].fillna("Missing")
			df[col] = df[col].astype(str).replace('nan', 'Missing')
		elif col_lower == 'qty':
			df[col] = df[col].fillna("0")
			df[col] = df[col].astype(str).replace('nan', '0')
		elif col_lower == 'date_sold':
			# Handle NaN, empty strings, and whitespace-only values
			df[col] = df[col].fillna("Missing")
			df[col] = df[col].astype(str)
			df[col] = df[col].str.strip()
			df[col] = df[col].replace('', 'Missing')
			df[col] = df[col].replace('nan', 'Missing')
	
	return df


data = handle_missing_values(data)

# Ensure all columns are strings to prevent NaN from being written as blank
data = data.astype(str)

# Debug: print the data to see what's there
print("Data before saving:")
print(data)

# Save cleaned data to CSV file
data.to_csv('data/processed/sales_data_clean.csv', index=False)
print("\nCleaned data saved to data/processed/sales_data_clean.csv")
