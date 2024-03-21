import pandas as pd

class DataTransform:
    @staticmethod
    def convert_to_datetime(df, columns):
        """
        Convert specified columns to datetime format.

        Args:
        - df (pd.DataFrame): Pandas DataFrame containing the data.
        - columns (list): List of column names to convert to datetime.

        Returns:
        - pd.DataFrame: Pandas DataFrame with specified columns converted to datetime.
        """
        for col in columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
        return df

    @staticmethod
    def convert_to_categorical(df, columns):
        """
        Convert specified columns to categorical format.

        Args:
        - df (pd.DataFrame): Pandas DataFrame containing the data.
        - columns (list): List of column names to convert to categorical.

        Returns:
        - pd.DataFrame: Pandas DataFrame with specified columns converted to categorical.
        """
        for col in columns:
            if col in df.columns:
                df[col] = df[col].astype('category')
        return df
    
#from data_transform import DataTransform