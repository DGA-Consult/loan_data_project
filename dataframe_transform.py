import pandas as pd

class DataFrameTransform:
    @staticmethod
    def count_null_values(df):
        """
        Count NULL values in each column of the DataFrame.

        Args:
        - df (pd.DataFrame): Pandas DataFrame.

        Returns:
        - pd.Series: Series containing count of NULL values in each column.
        """
        return df.isnull().sum()

    @staticmethod
    def drop_columns(df, columns):
        """
        Drop columns from the DataFrame.

        Args:
        - df (pd.DataFrame): Pandas DataFrame.
        - columns (list): List of column names to be dropped.

        Returns:
        - pd.DataFrame: DataFrame with specified columns dropped.
        """
        return df.drop(columns=columns, axis=1)

    @staticmethod
    def impute_null_values(df, strategy='median'):
        """
        Impute NULL values in the DataFrame columns.

        Args:
        - df (pd.DataFrame): Pandas DataFrame.
        - strategy (str): Imputation strategy. Default is 'median'.

        Returns:
        - pd.DataFrame: DataFrame with NULL values imputed.
        """
        if strategy == 'median':
            return df.fillna(df.median())
        elif strategy == 'mean':
            return df.fillna(df.mean())
        else:
            raise ValueError("Invalid imputation strategy. Choose from 'median' or 'mean'.")
