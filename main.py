import numpy as np
import yaml
import matplotlib.pyplot as plt
from db_utils import RDSDatabaseConnector, load_data
from dataframe_info import DataFrameInfo
from dataframe_transform import DataFrameTransform
from plotter import Plotter
from skewness_utils import SkewnessAnalyzer, SkewnessTransformer

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
    df = transformer.drop_missing_values()  # Example: Drop columns with missing values exceeding threshold
    df = transformer.fill_missing_values(strategy='mean')  # Example: Fill missing values with mean

    # Use Plotter to visualize insights from the data
    plotter = Plotter(df)
    plotter.plot_histogram(df.loan_amount, title="Histogram of loan amount")
else:
    print("Failed to load data. Check the file path and try again.")

# Using DataFrameInfo methods extract info from df after imputation/transformation
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
skewness_analyzer = SkewnessAnalyzer(df)
skewed_columns = skewness_analyzer.identify_skewed_columns()
skewness_analyzer.visualize_skewed_data(plotter)

# Step 2: Transform skewed columns
skewness_transformer = SkewnessTransformer(df, skewed_columns)
transformed_df = skewness_transformer.transform_skewed_columns()

# Step 3: Visualize the transformed data
plotter = Plotter(transformed_df)
numeric_columns = transformed_df.select_dtypes(include=np.number).columns
for col in numeric_columns:
    best_transformation = skewness_transformer.find_best_transformation(col)
    try:
        transformed_col = skewness_transformer.transform_column(col, best_transformation)
        plot_title = f'{col}_Transformed (Best Transformation: {best_transformation})'
        plotter.plot_histogram(transformed_col.values, title=plot_title, show=False)
    except ValueError as e:
        print(f"Error processing column '{col}': {e}")
        plot_title = f'{col}_Transformed (Transformation Failed)'
        plotter.plot_histogram(transformed_col.values, title=plot_title, show=False)

# Step 4: Optionally, save a separate copy of the transformed DataFrame
transformed_df.to_csv('transformed_loan_data.csv', index=False)


        
