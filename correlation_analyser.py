import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

class CorrelationAnalyser:
    def __init__(self, df):
        self.df = df
        
    def compute_correlation_matrix(self):
        numeric_df = self.df.select_dtypes(include=np.number)  # Select only numeric columns
        return numeric_df.corr()
    
    def visualize_correlation_matrix(self):
        correlation_matrix = self.compute_correlation_matrix()
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
        plt.title('Correlation Matrix')
        plt.show()
    
    def identify_highly_correlated_columns(self, correlation_matrix, threshold=0.8):
        """
        Identify highly correlated columns based on the correlation matrix and threshold.
        """
        highly_correlated_columns = []
        for i in range(len(correlation_matrix.columns)):
            for j in range(i):
                col1 = correlation_matrix.columns[i]
                col2 = correlation_matrix.index[j]
                correlation = correlation_matrix.iloc[i, j]
                if abs(correlation) > threshold:
                    highly_correlated_columns.append((col1, col2, correlation))
        return highly_correlated_columns
    
    def remove_highly_correlated_columns(self, threshold=0.8):
        correlated_pairs = self.identify_highly_correlated_columns(threshold)
        columns_to_remove = set()
        for pair in correlated_pairs:
            columns_to_remove.add(pair[1])  # Removing the second column in each correlated pair
        self.df.drop(columns=columns_to_remove, inplace=True)