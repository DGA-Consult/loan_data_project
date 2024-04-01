import matplotlib.pyplot as plt
import seaborn as sns

class Plotter:
    def __init__(self, df):
        """
        Initialize the Plotter instance.

        Args:
        - df (pd.DataFrame): Pandas DataFrame.
        """
        self.df = df

    def plot_histogram(self, column):
        """
        Plot a histogram for the specified column.

        Args:
        - column (str): Name of the column to plot.
        """
        plt.figure(figsize=(10, 6))
        sns.histplot(self.df[column], kde=True)
        plt.title(f'Histogram of {column}')
        plt.xlabel(column)
        plt.ylabel('Frequency')
        plt.show()

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