import pandas as pd

class DataFrameInfo:
    def __init__(self, df):
        """
        Initialize the DataFrameInfo instance.

        Args:
        - df (pd.DataFrame): Pandas DataFrame.
        """
        self.df = df

    def describe_columns(self):
        """
        Describe all columns in the DataFrame to check their data types.
        """
        return self.df.dtypes

    def extract_statistics(self):
        """
        Extract statistical values: median, standard deviation, and mean from the columns and the DataFrame.
        """
        return self.df.describe()

    def count_distinct_values(self):
        """
        Count distinct values in categorical columns.
        """
        return self.df.select_dtypes(include='category').nunique()

    def print_shape(self):
        """
        Print out the shape of the DataFrame.
        """
        print("Shape of the DataFrame:", self.df.shape)

    def count_null_values(self):
        """
        Generate a count/percentage count of NULL values in each column.
        """
        null_count = self.df.isnull().sum()
        null_percentage = (null_count / len(self.df)) * 100
        return pd.DataFrame({'Null Count': null_count, 'Null Percentage': null_percentage})

    # Add any other methods you may find useful for DataFrame information extraction
