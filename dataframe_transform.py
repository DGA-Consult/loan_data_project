import pandas as pd

class DataFrameTransform:
    @staticmethod
    def impute_missing_values(df, strategy='median'):
        """
        Impute missing values in the DataFrame.

        Args:
        - df (pd.DataFrame): Pandas DataFrame.
        - strategy (str): Imputation strategy. Default is 'median'.

        Returns:
        - pd.DataFrame: DataFrame with missing values imputed.
        """
        if strategy == 'median':
            return df.fillna(df.median())
        elif strategy == 'mean':
            return df.fillna(df.mean())
        elif strategy == 'mode':
            return df.fillna(df.mode().iloc[0])
        else:
            raise ValueError("Invalid imputation strategy. Choose from 'median', 'mean', or 'mode'.")