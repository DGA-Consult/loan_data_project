# db_utils.py

import pandas as pd
import psycopg2  # Assuming PostgreSQL database
import yaml
import sqlalchemy
from sqlalchemy import create_engine

class RDSDatabaseConnector:
    def __init__(self, credentials):
        """
        Initialize the RDSDatabaseConnector instance.

        Args:
        - credentials (dict): Dictionary containing the database credentials.
        """
        self.host = credentials['RDS_HOST']
        self.port = credentials['RDS_PORT']
        self.database = credentials['RDS_DATABASE']
        self.user = credentials['RDS_USER']
        self.password = credentials['RDS_PASSWORD']
        self.engine = None

    def connect(self):
        try:
            connection_string = f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
            self.engine = sqlalchemy.create_engine(connection_string)
            print("Connected to the database")
        except Exception as e:
            print("Error connecting to the database:", e)

    def disconnect(self):
        if self.engine:
            self.engine.dispose()
            print("Disconnected from the database")
    
    def extract_data(self, table_name):
        """
        Extract data from the specified table in the RDS database and return it as a Pandas DataFrame.

        Args:
        - table_name (str): Name of the table to extract data from.

        Returns:
        - pd.DataFrame: Pandas DataFrame containing the extracted data.
        """
        if self.engine is None:
            print("Error: Engine is not initialized.")
            return None

        query = f"SELECT * FROM {table_name}"
        try:
            with self.engine.connect() as connection:
                df = pd.read_sql_query(query, connection)
                print(f"Data extracted from table '{table_name}'")
                return df
        except Exception as e:
            print("Error executing SQL query:", e)
            return None

    def save_to_csv(self, df, file_path):
        """
        Save the DataFrame to a CSV file.

        Args:
        - df (pd.DataFrame): Pandas DataFrame to be saved.
        - file_path (str): File path to save the CSV file.
        """
        try:
            df.to_csv(file_path, index=False)
            print(f"Data saved to '{file_path}'")
        except Exception as e:
            print("Error saving data to CSV file:", e)

def load_credentials(self, file_path):
    """
    Load database credentials from a YAML file.

    Args:
    - file_path (str): Path to the YAML file containing the credentials.

    Returns:
    - dict: Dictionary containing the database credentials.
        """
    with open(file_path, 'r') as file:
        credentials = yaml.safe_load(file)
    return credentials

if __name__ == "__main__":
    # Load database credentials
    # credentials = load_credentials('credentials.yaml')

    # Create an instance of RDSDatabaseConnector
    # rds_connector = RDSDatabaseConnector(
        # host=credentials['RDS_HOST'],
        # port=credentials['RDS_PORT'],
        # database=credentials['RDS_DATABASE'],
        # user=credentials['RDS_USER'],
        # password=credentials['RDS_PASSWORD']
    # )

    # Connect to the database
    # rds_connector.connect()

    # Now can use the rds_connector object to interact with the RDS database

    # Load database credentials
    credentials = load_credentials('credentials.yaml')

    # Create an instance of RDSDatabaseConnector
    rds_connector = RDSDatabaseConnector(credentials)

    # Connect to the database
    rds_connector.connect()

    # Initialize the SQLAlchemy engine
    rds_connector.initialize_engine()

    # Extract data from the loan_payments table and store it in a DataFrame
    payments_df = rds_connector.extract_data('loan_payments')

    # Display the DataFrame
    print(payments_df)

    # Save the DataFrame to a CSV file
    rds_connector.save_to_csv(payments_df, 'loan_payments.csv')

def load_data(file_path):
    """
    Load data from a CSV file into a Pandas DataFrame.

    Args:
    - file_path (str): File path to the CSV file.

    Returns:
    - pd.DataFrame: Pandas DataFrame containing the loaded data.
    """
    try:
        df = pd.read_csv(file_path)
        print("Data loaded successfully")
        print("Shape of the data:", df.shape)
        return df
    except Exception as e:
        print("Error loading data:", e)
        return None

# Example usage:
file_path = 'loan_payments.csv'  # Replace with the actual file path
data_df = load_data(file_path)
