import pandas as pd
import os

class Price():
    def list( min_val, max_val):
        file_path = os.path.join(os.path.dirname(__file__), 'NSE.xlsx')

        try:
            print("Reading from:", file_path)
            df = pd.read_excel(file_path, sheet_name='NSE')
            df.iloc[:, 1] = pd.to_numeric(df.iloc[:, 1], errors='coerce')
        except Exception as e:
            return []

        df = df.dropna(subset=[df.columns[1]])

        if min_val > max_val:
            return []

        filtered_names = df[(df.iloc[:, 1] >= min_val) & (df.iloc[:, 1] <= max_val)].iloc[:, 0].tolist()

        if filtered_names:
            return filtered_names
        else:
            return []

# Example usage:

