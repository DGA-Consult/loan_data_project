class DataFrameTransform:
    def __init__(self, df):
        """
        Initialize the DataFrameTransform instance.

        Args:
        - df (pd.DataFrame): Pandas DataFrame.
        """
        self.df = df

    def drop_missing_values(self, threshold=0.5):
        """
        Drop columns with missing values exceeding the threshold.

        Args:
        - threshold (float): Threshold percentage of missing values. Default is 50%.

        Returns:
        - pd.DataFrame: DataFrame with columns dropped.
        """
        null_percentage = (self.df.isnull().sum() / len(self.df)) * 100
        columns_to_drop = null_percentage[null_percentage > threshold].index
        self.df.drop(columns=columns_to_drop, inplace=True)
        return self.df

    def fill_missing_values(self, strategy):
        """
        Fill missing values using specified strategy.

        Args:
        - strategy (str): Strategy to fill missing values. Options: 'mean', 'median', 'mode'. Default is 'mean'.

        Returns:
        - pd.DataFrame: DataFrame with missing values filled.
        """
        if strategy == 'mean':
            self.df.fillna(self.df.mean(numeric_only=True), inplace=True)
        elif strategy == 'median':
            self.df.fillna(self.df.median(numeric_only=True), inplace=True)
        elif strategy == 'mode':
            # Fill missing values with the most frequent value in each column
            self.df = self.df.apply(lambda x: x.fillna(x.value_counts().index[0]) if x.dtype == 'O' else x)
        else:
            print("Invalid strategy. Please choose from 'mean', 'median', or 'mode'.")
        return self.df
    
     