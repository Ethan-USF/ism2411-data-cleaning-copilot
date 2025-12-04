import re
import sys
import os
from pathlib import Path
import pandas as pd
import numpy as np


# Copilot-assisted function: Load data from a CSV file into a pandas DataFrame.
# This function should read the CSV at `file_path` and return a DataFrame.
def load_data(file_path: str):
	try:
		return pd.read_csv(file_path)
	except Exception:
		# Try a more permissive read (common encoding issues)
		return pd.read_csv(file_path, encoding='utf-8', engine='python')


# Copilot-assisted function: Standardize column names.
# This function should lowercase column names, strip surrounding whitespace,
# and replace non-alphanumeric characters with underscores.
def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
	df = df.copy()
	new_cols = []
	for col in df.columns:
		c = str(col).strip().lower()
		c = re.sub(r"[^0-9a-z]+", '_', c)
		c = c.strip('_')
		new_cols.append(c)
	df.columns = new_cols
	return df


def strip_whitespace(df: pd.DataFrame) -> pd.DataFrame:
	"""Strip leading/trailing whitespace from product and category columns.

	The function finds columns with names containing 'product' or 'category'
	(after column cleaning) and applies string strip to them.
	"""
	df = df.copy()
	for col in df.columns:
		if 'product' in col or 'category' in col:
			df[col] = df[col].astype(str).str.strip()
	return df


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
	"""Handle missing prices and quantities consistently.

	- Price-like columns (column name contains 'price') are converted to numeric
	  and missing values are filled with the column median.
	- Quantity-like columns (contains 'qty' or 'quantity') are converted to
	  numeric and missing values are filled with 0.
	"""
	df = df.copy()
	price_cols = [c for c in df.columns if 'price' in c]
	qty_cols = [c for c in df.columns if 'qty' in c or 'quantity' in c]

	for c in price_cols:
		df[c] = pd.to_numeric(df[c], errors='coerce')
		median = df[c].median()
		df[c].fillna(median, inplace=True)

	for c in qty_cols:
		df[c] = pd.to_numeric(df[c], errors='coerce')
		df[c].fillna(0, inplace=True)

	return df


def remove_invalid_rows(df: pd.DataFrame) -> pd.DataFrame:
	"""Remove rows with clearly invalid numeric values.

	Specifically removes rows with negative prices or negative quantities
	(for any column that looks like a price or a quantity).
	"""
	df = df.copy()
	price_cols = [c for c in df.columns if 'price' in c]
	qty_cols = [c for c in df.columns if 'qty' in c or 'quantity' in c]

	mask = pd.Series(True, index=df.index)
	for c in price_cols:
		mask &= df[c].ge(0)
	for c in qty_cols:
		mask &= df[c].ge(0)

	return df[mask].copy()


def save_clean_data(df: pd.DataFrame, out_path: str):
	out_dir = os.path.dirname(out_path)
	if out_dir:
		Path(out_dir).mkdir(parents=True, exist_ok=True)
	df.to_csv(out_path, index=False)


def main(input_path: str, output_path: str):
	df = load_data(input_path)
	df = clean_column_names(df)
	df = strip_whitespace(df)
	df = handle_missing_values(df)
	df = remove_invalid_rows(df)
	save_clean_data(df, output_path)
	print(f"Saved cleaned data to {output_path}")


if __name__ == '__main__':
	default_input = 'C:/Users/silly/Downloads/sales_data_raw.csv'
	default_output = 'data/processed/sales_data_clean.csv'
	in_path = sys.argv[1] if len(sys.argv) > 1 else default_input
	out_path = sys.argv[2] if len(sys.argv) > 2 else default_output
	main(in_path, out_path)
