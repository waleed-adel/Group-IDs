#!/usr/bin/python3

import numpy as np
import pandas as pd

# Define the number of rows needed to make the file large (~100MB)
num_rows = (10**5)*5  # Adjust this to generate a large file size

# Define the number of columns and the specific column for Identifier
num_columns = 50
identifier_column = 'Identifier'

# Generate unique identifiers (e.g., ID_0, ID_1, ..., ID_999999)
identifiers = [f'ID_{i}' for i in range(num_rows)]

# Create integer data for Column_1 with values between 0 and 100 (inclusive)
data_1 = {f'Column_1': np.random.randint(0, 101, num_rows)}
data_2 = {f'Column_1': np.random.randint(0, 101, num_rows)}

# Create random float data for the remaining columns
for i in range(2, num_columns + 1):
    data_1[f'Column_{i}'] = np.random.rand(num_rows)
    data_2[f'Column_{i}'] = np.random.rand(num_rows)

# Add the Identifier column
data_1[identifier_column] = identifiers
data_2[identifier_column] = identifiers

# Create the DataFrame
large_df_unique_1 = pd.DataFrame(data_1)
large_df_unique_2 = pd.DataFrame(data_2)

# Save the DataFrame as a large CSV file
csv_large_file_path = '../test_data/large_group_ids.csv'
csv_large_file_diff_path = '../test_data/large_group_ids_diff.csv'
large_df_unique_1.to_csv(csv_large_file_path, index=False)
large_df_unique_2.to_csv(csv_large_file_diff_path)

print(f"CSV file generated: {csv_large_file_path}")
print(f"CSV file generated: {csv_large_file_diff_path}")
