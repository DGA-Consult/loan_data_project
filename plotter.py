import matplotlib.pyplot as plt
import seaborn as sns

class Plotter:
    @staticmethod
    def plot_missing_values(df):
        """
        Plot missing values in the DataFrame.

        Args:
        - df (pd.DataFrame): Pandas DataFrame.

        Returns:
        - None
        """
        plt.figure(figsize=(10, 6))
        sns.heatmap(df.isnull(), cbar=False, cmap='viridis')
        plt.title('Missing Values in DataFrame')
        plt.show()