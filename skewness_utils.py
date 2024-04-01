import pandas as pd
import numpy as np
from scipy.stats import skew
from plotter import Plotter  # Assuming you have a Plotter class

class SkewnessAnalyzer:
    def __init__(self, df):
        self.df = df

    def identify_skewed_columns(self, skew_threshold=0.5):
        self.skewed_columns = self.df.apply(lambda x: x.skew()).sort_values(ascending=False)
        self.skewed_columns = self.skewed_columns[abs(self.skewed_columns) > skew_threshold]
        return self.skewed_columns.index.tolist()

    def visualize_skewed_data(self, plotter):
        for col in self.skewed_columns:
            plotter.plot_histogram(col)

class SkewnessTransformer:
    def __init__(self, df):
        self.df = df

    def transform_skewed_columns(self, method='log'):
        transformed_df = self.df.copy()
        for col in self.df.columns:
            if col in self.skewed_columns:
                if method == 'log':
                    transformed_df[col] = np.log1p(transformed_df[col])
                elif method == 'sqrt':
                    transformed_df[col] = np.sqrt(transformed_df[col])
                elif method == 'boxcox':
                    transformed_df[col] = boxcox(transformed_df[col] + 1)[0]
        return transformed_df
