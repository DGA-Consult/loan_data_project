import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

class Plotter:
    def __init__(self, df):
        """
        Initialize the Plotter instance.

        Args:
        - df (pd.DataFrame): Pandas DataFrame.
        """
        self.df = df

    def plot_histogram(self, data, title=None, show=True):
        """
        Plot a histogram for the specified data.

        Args:
        - data (DataFrame or Series): Data to plot.
        - title (str): Title of the plot. Default is None.
        - show (bool): Whether to display the plot on the screen. Default is True.

        Returns:
        - ax (Axes): The Axes object of the plot.
        """
        plt.figure(figsize=(10, 6))
        ax = sns.histplot(data, kde=True)
        plt.title(title if title else 'Histogram')
        plt.xlabel('Value')
        plt.ylabel('Frequency')
        if show:
            plt.show()
        else:
            return ax  # Return the Axes object
    
    def plot_boxplot(self, column):
        """
        Plot a boxplot for the specified column.

        Args:
        - column (str): Name of the column to plot.
        """
        plt.figure(figsize=(10, 6))
        sns.boxplot(x=self.df[column])
        plt.title(f'Boxplot of {column}')
        plt.xlabel(column)
        plt.show()