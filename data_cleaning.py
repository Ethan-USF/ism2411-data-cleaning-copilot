import pandas as pd
import numpy as np
from pathlib import Path

csv_file_path = Path('C:/Users/silly/Downloads/sales_data_raw.csv')
data = pd.read_csv(csv_file_path)
print(data)