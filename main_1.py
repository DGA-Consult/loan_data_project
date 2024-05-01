import numpy as np
import pandas as pd
import seaborn as sns
import yaml
import matplotlib.pyplot as plt
from db_utils import RDSDatabaseConnector, load_data
from dataframe_info import DataFrameInfo
from dataframe_transform import DataFrameTransform
from plotter import Plotter
from skewness_utils import SkewnessAnalyzer, SkewnessTransformer
from correlation_analyser import CorrelationAnalyser 

# Load database credentials from the YAML file
credentials_file = 'credentials.yaml'

# Load the credentials
with open(credentials_file, 'r') as file:
    credentials = yaml.safe_load(file)

# Create an instance of RDSDatabaseConnector
rds_connector = RDSDatabaseConnector(credentials)

# Connect to the database
rds_connector.connect()

# Extract data from the RDS database
table_name = 'loan_payments'
df = rds_connector.extract_data(table_name)

# Save the extracted data to a CSV file
if df is not None:
    file_path = 'loan_payments.csv'
    rds_connector.save_to_csv(df, file_path)

# Disconnect from the database
rds_connector.disconnect()

# Call the load_data function to load the data
df = load_data(file_path)

# Check if data is loaded successfully
if df is not None:
    print(df.head())  # Print the first few rows of the DataFrame
    # Do further processing or analysis with the loaded DataFrame
else:
    print("Failed to load data. Check the file path and try again.")

# Use DataFrameInfo to extract information about the DataFrame
df_info = DataFrameInfo(df)

# Using DataFrameInfo methods
print("Column Data Types:")
print(df_info.describe_columns())
print()

print("Statistical Values:")
print(df_info.extract_statistics())
print()

print("Distinct Values in Cat'egorical Columns:")
print(df_info.count_distinct_values())
print()

print("Null Values in Each Column:")
print(df_info.count_null_values())
print()

print("Shape of the DataFrame:")
df_info.print_shape()

if df is not None:
    # Use DataFrameTransform to handle missing values
    transformer = DataFrameTransform(df)
    df_handle_missing_values = transformer.drop_missing_values()  # Example: Drop columns with missing values exceeding threshold
    df_handle_missing_values = transformer.fill_missing_values(strategy='mean')  # Example: Fill missing values with mean

    # Use Plotter to visualize insights from the data
    plotter = Plotter(df_handle_missing_values)
    plotter.plot_histogram(df_handle_missing_values.loan_amount, title="Histogram of loan amount")
else:
    print("Failed to load data. Check the file path and try again.")

# Using DataFrameInfo methods extract info from df after imputation/transformation
    
df_info = DataFrameInfo(df_handle_missing_values)

print("Column Data Types:")
print(df_info.describe_columns())
print()

print("Statistical Values:")
print(df_info.extract_statistics())
print()

print("Distinct Values in Categorical Columns:")
print(df_info.count_distinct_values())
print()

print("Null Values in Each Column:")
print(df_info.count_null_values())
print()

print("Shape of the DataFrame:")
df_info.print_shape()

# now treat skew data

# Step 1: Identify skewed columns and visualize data
skewness_analyzer = SkewnessAnalyzer(df_handle_missing_values)
skewed_columns = skewness_analyzer.identify_skewed_columns()
skewness_analyzer.visualize_skewed_data(plotter)

# Step 2: Transform skewed columns
skewness_transformer = SkewnessTransformer(df_handle_missing_values, skewed_columns)
transformed_df = skewness_transformer.transform_skewed_columns()

# Step 3: Save the transformed data plots as PNG files
plotter = Plotter(transformed_df)
for col in transformed_df.select_dtypes(include=np.number).columns:
    best_transformation = skewness_transformer.find_best_transformation(col)
    try:
        plot_title = f'{col}_Transformed (Best Transformation: {best_transformation})'
        plotter.plot_histogram(col, show=False)  # Plot the histogram without displaying it
        plt.title(plot_title)  # Set the title of the plot
        plt.savefig(f'{plot_title}.png')  # Save the plot as an image file
        plt.close()  # Close the plot window
    except ValueError as e:
        print(f"Error processing column '{col}': {e}")

# Step 4: Optionally, save a separate copy of the transformed DataFrame
transformed_df.to_csv('transformed_loan_data.csv', index=False)

# now treat outliers if any are found

# Step 1: Visualize the data to identify outliers
plotter = Plotter(transformed_df)
plotter.plot_boxplot('loan_amount')  # Example: Plot boxplot to visualize outliers in 'loan_amount' column

# Step 2: Remove outliers using DataFrameTransform class for all numeric columns
transformer = DataFrameTransform(transformed_df)
df_without_outliers = transformed_df.copy()  # Create a copy of the DataFrame to preserve the original data

# Iterate through all numeric columns and remove outliers
for col in df_without_outliers.select_dtypes(include=np.number).columns:
    df_without_outliers = transformer.remove_outliers(df_without_outliers, column=col)  # Remove outliers from each numeric column

# Step 3: Re-visualize the data after removing outliers
plotter = Plotter(df_without_outliers)
for col in df_without_outliers.select_dtypes(include=np.number).columns:
    plot_title = f'{col}_transformed_and_outliers_removed'
    plotter.plot_histogram(col, show=False)  # Plot the histogram without displaying it
    plt.title(plot_title)  # Set the title of the plot
    plt.savefig(f'{plot_title}.png')  # Save the plot as an image file
    plt.close()  # Close the plot window

# Step 4: Save the data with outliers removed to a separate CSV file
file_path_without_outliers = 'loan_payments_without_outliers.csv'
rds_connector.save_to_csv(df_without_outliers, file_path_without_outliers)
        
# now calculate correlations, identify and remove highly correlated variables

# Step 1: Compute the correlation matrix for the dataset and visualize it
correlation_analyser = CorrelationAnalyser(df)
correlation_matrix = correlation_analyser.compute_correlation_matrix()
correlation_analyser.visualize_correlation_matrix()

# Step 2: Identify highly correlated columns
# Define correlation threshold
correlation_threshold = 0.8

# Find highly correlated columns
highly_correlated_columns = correlation_analyser.identify_highly_correlated_columns(correlation_matrix, threshold=correlation_threshold)
for col1, col2, correlation in highly_correlated_columns:
    print(f"Columns '{col1}' and '{col2}' have correlation {correlation:.2f}")

# Step 3: Remove highly correlated columns from the dataset
# df.drop(columns=columns_to_remove, inplace=True)
    

# Next, look at the current state of the loan book
    
from loan_book_analyzer import LoanBookAnalyzer

# Step 1: Instantiate LoanBookAnalyzer with loan data
analyzer = LoanBookAnalyzer(df)

# Step 2: Calculate percentage of recovered amounts
analyzer.calculate_percentage_recovered()

# Step 3: Visualize percentage of recovered amounts against investor funding
analyzer.visualize_recovery_percentage()

# Step 4: Estimate percentage of total amount to be recovered up to six months in the future
recovery_amounts = analyzer.estimate_recovery_percentage_six_months()

# Next, calculate the percentage of loans that have been a loss to the company
charged_off_percentage = analyzer.calculate_charged_off_percentage()
total_amount_charged_off = analyzer.calculate_total_amount_charged_off() 