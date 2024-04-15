import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import skew, boxcox
from plotter import Plotter

class SkewnessAnalyzer:
    def __init__(self, df):
        self.df = df
        self.skewed_columns = None

    def identify_skewed_columns(self):
        # Exclude non-numeric columns from skewness calculation
        numeric_columns = self.df.select_dtypes(include=[np.number]).columns
        self.skewed_columns = self.df[numeric_columns].apply(lambda x: x.skew()).sort_values(ascending=False)
        return self.skewed_columns

    def visualize_skewed_data(self, plotter):
        numeric_columns = self.df.select_dtypes(include=[np.number]).columns
        for col in self.skewed_columns.index:
            if col in numeric_columns:
                plot_title = f'{col}_skewed_histogram'
                plotter.plot_histogram(col, show=False)  # Plot the histogram without displaying it
                plt.title(plot_title)  # Set the title of the plot
                plt.savefig(f'{plot_title}.png')  # Save the plot as an image file
                plt.close()  # Close the plot window

class SkewnessTransformer:
    def __init__(self, df, skewed_columns, threshold=0.5):
        """
        Initialize the SkewnessTransformer instance.

        Args:
        - df (pd.DataFrame): Pandas DataFrame.
        - skewed_columns (pd.Series): Series containing skewness values for each column.
        - threshold (float): Threshold for considering a column as skewed. Default is 0.5.
        """
        self.df = df
        self.skewed_columns = skewed_columns
        self.threshold = threshold

    def transform_skewed_columns(self):
        """
        Transform skewed columns using the best transformation method.

        Returns:
        - pd.DataFrame: Transformed DataFrame.
        """
        transformed_df = self.df.copy()
        for col in self.skewed_columns.index:
            best_method = self.find_best_transformation(col)
            if best_method:
                transformed_df[col] = self.apply_transformation(transformed_df[col], best_method)
        return transformed_df

    def find_best_transformation(self, column):
        skew_before = abs(self.df[column].skew())
        skewness_dict = {}

        if skew_before > self.threshold:
            # Try 'log' transformation
            log_skew = abs(np.log1p(self.df[column]).skew())
            skewness_dict['log'] = log_skew

            # Try 'sqrt' transformation
            sqrt_skew = abs(np.sqrt(self.df[column]).skew())
            skewness_dict['sqrt'] = sqrt_skew

            # Try 'boxcox' transformation
            try:
                boxcox_skew = abs(pd.Series(stats.boxcox(self.df[column])[0]).skew())
                skewness_dict['boxcox'] = boxcox_skew
            except:
                pass

            # Find the method with the smallest absolute skewness
            best_method = min(skewness_dict, key=skewness_dict.get)
            skew_after = skewness_dict[best_method]

            # Return the best method if absolute skewness is reduced
            if skew_after < skew_before:
                return best_method
        return None

    def transform_column(self, column, transformation):
        """
        Transform a column using the specified transformation method.

        Args:
        - column (str): Name of the column to transform.
        - transformation (str): Transformation method to apply.

        Returns:
        - transformed_column (pandas Series): Transformed column.
        """
        if transformation == 'log':
            transformed_column = np.log1p(self.df[column])
        elif transformation == 'sqrt':
            transformed_column = np.sqrt(self.df[column])
        elif transformation == 'boxcox':
            transformed_column, _ = boxcox(self.df[column] + 1)  # Adding 1 to handle zero and negative values
        else:
            raise ValueError("Invalid transformation method.")

        return pd.Series(transformed_column.values, index=self.df.index, name=column)

    def apply_transformation(self, column, method):
        """
        Apply the specified transformation method to the column.

        Args:
        - column (pd.Series): Column to be transformed.
        - method (str): Transformation method. Options: 'log', 'sqrt', 'boxcox'.

        Returns:
        - pd.Series: Transformed column.
        """
        if method == 'log':
            return np.log1p(column)
        elif method == 'sqrt':
            return np.sqrt(column)
        elif method == 'boxcox':
            return pd.Series(stats.boxcox(column)[0])
        else:
            return column
